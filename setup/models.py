from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
import setup.defaults as defaults
from xml.etree.ElementTree import Element, tostring
import xml.etree.ElementTree as ET
import requests
from django.contrib.auth.models import User
from recurrence.fields import RecurrenceField
from macaddress.fields import MACAddressField
from utils.advutils import get_logger

import json

logger = get_logger('iot_settings')

class SignalType(models.Model):
    PROTOCOL_TYPE = (
        ('Q', 'MQTT'),
        ('M', 'ModBus'),
    )
    name = models.CharField(max_length=60)
    class_name = models.CharField(max_length=200)
    protocol = models.CharField(max_length=1, choices=PROTOCOL_TYPE)
    create_date = models.DateTimeField('create datetime', auto_now=False,
                                       auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)

    def __str__(self):
        return self.name


class SignalUnit(models.Model):
    descr = models.CharField(max_length=60)
    create_date = models.DateTimeField('create date', auto_now=False,
                                       auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)

    def __str__(self):
        return self.descr


class Signal(models.Model):
    unit = models.ForeignKey(SignalUnit, on_delete=models.PROTECT)
    type = models.ForeignKey(SignalType, on_delete=models.PROTECT)
    descr = models.CharField(max_length=300)
    create_date = models.DateTimeField('create date', auto_now=False,
                                       auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)

    def __str__(self):
        return self.descr


class DeviceType(models.Model):
    descr = models.CharField(max_length=300)
    create_date = models.DateTimeField('create date', auto_now=False,
                                       auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)

    def __str__(self):
        return self.descr


class IOSignalsDeviceType(models.Model):
    IO_TYPE = (
        ('I', 'Input'),
        ('O', 'Output'),
    )
    device = models.ForeignKey(DeviceType, related_name='io_signals',
                               on_delete=models.CASCADE)
    signal = models.ForeignKey(Signal, on_delete=models.PROTECT)
    i_o = models.CharField(max_length=1, choices=IO_TYPE)

    def __str__(self):
        return self.device.__str__() + '- signal:' + self.signal.__str__() + ' type:' + self.i_o


class MonitoringDevice(models.Model):
    device_type = models.ForeignKey(DeviceType, on_delete=models.PROTECT)
    descr = models.CharField(max_length=100, null=True, blank=True)
    serial = models.CharField(max_length=40, null=True, blank=True)
    mac_address = MACAddressField(null=True, blank=True, integer=False)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    create_date = models.DateTimeField('create date', auto_now=False,
                                       auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)

    def clean(self):
        """
        This function verifies that the user has provided at least one of the key field for 
        the measuring device
        """
        if (not self.serial) and (not self.mac_address) and (
        not self.ip_address):
            raise ValidationError(
                "A key for the measuring device has not been provided. Please fill the serial or mac_addrees or ip_address")

    def __str__(self):
        return self.descr


class MeasuredEntity(models.Model):
    MEASURED_ENTITY_TYPE = (
        ('M', 'Machine'),
        ('P', 'Plant'),
    )
    code = models.CharField(max_length=180, null=False, blank=False)
    descr = models.CharField(max_length=200)
    type = models.CharField(max_length=1, choices=MEASURED_ENTITY_TYPE,
                            default='M')
    serial = models.CharField(max_length=60, null=True, blank=True)
    create_date = models.DateTimeField('create datetime', auto_now=False,
                                       auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)

    def __str__(self):
        return self.code + ' ' + self.descr

    def __unicode__(self):
        return self.code


class PlantHostSystem(MeasuredEntity):
    id_compania = models.CharField(max_length=60)
    id_sede = models.CharField(max_length=60)
    id_planta = models.CharField(max_length=60)


class MachineHostSystem(MeasuredEntity):
    id_compania = models.CharField(max_length=60)
    id_sede = models.CharField(max_length=60)
    id_planta = models.CharField(max_length=60)
    id_grupo_maquina = models.CharField(max_length=60)
    id_maquina = models.CharField(max_length=60)
    tasa_vel_esperada = models.FloatField(default=0)
    tiempo_esperado_config = models.FloatField(default=0)
    factor_conversion_kg_ciclo = models.FloatField(default=0)
    factor_conversion_mil_ciclo = models.FloatField(default=0)
    factor_conversion_emp_ciclo = models.FloatField(default=0)
    descripcion_sin_trabajo = models.CharField(max_length=200,
                                               default= 'sin_trabajo')

    @property
    def get_code(self):
        return str(
            self.id_compania + '-' + self.id_sede + '-' + self.id_planta \
            + '-' + self.id_grupo_maquina + '-' + self.id_maquina)


class InputOutputPort(models.Model):
    device = models.ForeignKey(MonitoringDevice, related_name='io_ports',
                               on_delete=models.CASCADE)
    port_label = models.CharField(max_length=60, default='COM1',
                                  help_text="This field must be included in the mqtt and modbus topic")
    signal_type = models.ForeignKey(Signal, on_delete=models.PROTECT)
    refresh_time_ms = models.IntegerField(default=5000,
                                          help_text="It specifies how often a new measured is obtained in milliseconds")
    measured_entity = models.ForeignKey(MeasuredEntity,
                                        related_name='measured_entity',
                                        blank=True, null=True,
                                        on_delete=models.SET_NULL)
    transformation_text = models.TextField(null=True, blank=True)

    def clean(self):
        if (self.transformation_text != None):
            if (len(self.transformation_text) > 0):
                dic = {'program': self.transformation_text,
                       'measured_entity': str(self.measured_entity.id)}
                jsondata = json.dumps(dic)
                url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(
                    defaults.PORT) + '/'
                url = url + defaults.CONTEXT_ROOT + '/'
                url = url + 'checker/transformation'
                try:
                    r = requests.put(url, data=jsondata)
                    if (r.status_code == 400):
                        raise ValidationError("Invalid language request")
                    else:
                        tree = ET.ElementTree(ET.fromstring(r.content))
                        root = tree.getroot()
                        for child in root:
                            lineNumber = child[0].text
                            positionInLine = child[1].text
                            message = child[2].text
                            raise ValidationError(
                                "Error in line:" + str(lineNumber) +
                                " character:" + str(positionInLine) + " " + str(
                                    message))
                except requests.exceptions.RequestException as e:
                    logger.info(e)
                    raise ValidationError(
                        "An error occurs when connecting to the Syntax Validation Server")

    def __str__(self):
        return self.port_label


class MeasuredEntityBehavior(models.Model):
    measure_entity = models.ForeignKey(MeasuredEntity, related_name='behaviors',
                                       on_delete=models.CASCADE)
    name = models.CharField(max_length=40, null=False, blank=False)
    descr = models.CharField(max_length=160, null=False, blank=False)
    behavior_text = models.TextField(null=True, blank=True)
    create_date = models.DateTimeField('create datetime', auto_now=False,
                                       auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)

    def clean(self):
        print('in clean')
        if len(self.behavior_text) > 0:
            dic = {'program': self.behavior_text,
                   'measured_entity': str(self.measure_entity.id)}
            jsondata = json.dumps(dic)
            url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(
                defaults.PORT) + '/'
            url = url + defaults.CONTEXT_ROOT + '/'
            url = url + 'checker/behavior'
            try:
                r = requests.put(url, data=jsondata)
                if (r.status_code == 400):
                    raise ValidationError("Invalid language request")
                else:
                    tree = ET.ElementTree(ET.fromstring(r.content))
                    root = tree.getroot()
                    for child in root:
                        lineNumber = child[0].text
                        positionInLine = child[1].text
                        message = child[2].text
                        raise ValidationError(
                            "Error in line:" + str(lineNumber) +
                            " character:" + str(positionInLine) + " " + str(
                                message))
            except requests.exceptions.RequestException as e:
                logger.info(e)
                raise ValidationError(
                    "An error occurs when connecting to the Syntax Validation Server")

    def delete(self, *args, **kwards):
        """
        Only deletes the behavior of not used in transformations.
        """
        # Verifies that the behavior is not called in any transformation
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(
            defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MeasuredEntity' + '/' + str(self.measure_entity.id)
        url = url + '/TransformationsUsingBehavior/' + str(self.id)
        try:
            r = requests.get(url)
            if (r.status_code == 200):
                json = r.json()
                if len(json) == 0:
                    super(MeasuredEntityBehavior, self).delete(*args, **kwards)
        except requests.exceptions.RequestException as e:
            logger.info(e)

    def __str__(self):
        return self.name + ' ' + self.descr


class MeasuredEntityStateBehavior(models.Model):
    STATE_BEHAVIOR_TYPE = (
        ('AR', 'Activity Registration'),
    )
    measure_entity = models.ForeignKey(MeasuredEntity,
                                       related_name='state_behaviors',
                                       on_delete=models.CASCADE)
    state_behavior_type = models.CharField(max_length=2,
                                           choices=STATE_BEHAVIOR_TYPE,
                                           default=0)
    descr = models.CharField(max_length=160, null=False, blank=False)
    behavior_text = models.TextField(null=True, blank=True)
    create_date = models.DateTimeField('create datetime', auto_now=False,
                                       auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)

    def clean(self):
        if len(self.behavior_text) > 0:
            dic = {'program': self.behavior_text,
                   'measured_entity': str(self.measure_entity.id)}
            jsondata = json.dumps(dic)
            url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(
                defaults.PORT) + '/'
            url = url + defaults.CONTEXT_ROOT + '/'
            url = url + 'checker/behavior'
            try:
                r = requests.put(url, data=jsondata)
                if (r.status_code == 400):
                    raise ValidationError("Invalid language request")
                else:
                    tree = ET.ElementTree(ET.fromstring(r.content))
                    root = tree.getroot()
                    for child in root:
                        lineNumber = child[0].text
                        positionInLine = child[1].text
                        message = child[2].text
                        raise ValidationError(
                            "Error in line:" + str(lineNumber) +
                            " character:" + str(positionInLine) + " " + str(
                                message))
            except requests.exceptions.RequestException as e:
                logger.info(e)
                raise ValidationError(
                    "An error occurs when connecting to the Syntax Validation Server")

    def __str__(self):
        return str(self.measure_entity) + '-' + self.descr


class MeasuredEntityScheduledEvent(models.Model):
    EVENT_TYPE = (
        ('AG', 'OEE Aggregation'),
    )
    measure_entity = models.ForeignKey(MeasuredEntity,
                                       related_name='schedule_event',
                                       on_delete=models.CASCADE)
    scheduled_event_type = models.CharField(max_length=2, choices=EVENT_TYPE,
                                            default=0)
    descr = models.CharField(max_length=160, null=False, blank=False)
    recurrences = RecurrenceField()
    day_time = models.TimeField('day_time', editable=True)
    create_date = models.DateTimeField('create datetime', auto_now=False,
                                       auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)


class MeasuredEntityGroup(models.Model):
    descr = models.CharField(max_length=160, null=False, blank=False)
    create_date = models.DateTimeField('create datetime', auto_now=False,
                                       auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)

    def __str__(self):
        return self.descr


class IdleReason(models.Model):
    IDLE_CLASSIFICATION = (
        ('A', 'Availability'),
        ('C', 'Capacity'),
        ('P', 'Performance'),
    )

    IDLE_DOWN = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )

    descr = models.CharField(max_length=160, null=False, blank=False)
    group_cd = models.CharField(max_length=60, null=True, blank=True)
    cause = models.CharField(max_length=60, null=True, blank=True)
    classification = models.CharField(max_length=1, choices=IDLE_CLASSIFICATION,
                                      default='A')
    down = models.CharField(max_length=1, choices=IDLE_DOWN, default='Y')
    create_date = models.DateTimeField('create datetime', auto_now=False,
                                       auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)

    def __str__(self):
        return self.descr


class IdleReasonHostSystem(IdleReason):
    id_compania = models.CharField(max_length=60)
    id_sede = models.CharField(max_length=60)
    id_planta = models.CharField(max_length=60)
    id_razon_parada = models.CharField(max_length=60)


class MeasuredEntityTransitionState(models.Model):
    STATE_OPTIONS = (
        ('O', 'Operating'),
        ('S', 'Schedule Down'),
        ('U', 'Unchedule Down'),
        ('D', 'Undefined'),
    )
    measure_entity = models.ForeignKey(MeasuredEntity,
                                       related_name='measured_states',
                                       on_delete=models.CASCADE)
    state_from = models.CharField(max_length=1, choices=STATE_OPTIONS,
                                  default='S')
    reason_code = models.ForeignKey(IdleReason, related_name='reasons',
                                    on_delete=models.PROTECT)
    behavior = models.ForeignKey(MeasuredEntityStateBehavior,
                                 on_delete=models.PROTECT)
    create_date = models.DateTimeField('create datetime', auto_now=False,
                                       auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)


class DisplayType(models.Model):
    COLOR_OPTIONS = (
        ('K', 'Black'),
        ('R', 'Red'),
        ('G', 'Green'),
        ('Y', 'Yellow'),
    )

    MODE_OPTIONS = (
        ('JO', 'Jump out'),
        ('ML', 'Move Left'),
        ('MR', 'Move Right'),
        ('SL', 'Scroll Left'),
        ('SR', 'Scroll Right'),
    )

    SPEED_OPTIONS = (
        ('0', 'Very Fast'),
        ('1', 'Fast'),
        ('2', 'Medium Fast'),
        ('3', 'Medium'),
        ('4', 'Medium Slow'),
        ('5', 'Slow'),
        ('6', 'Very Slow'),
    )

    LETTER_SIZE = (
        ('0', 'Normal 5 (5X5)'),
        ('1', 'Normal 7 (6X7)'),
        ('2', 'Normal 14 (8X14)'),
        ('3', 'Normal 15 (9X15)'),
        ('4', 'Normal 16 (9X16)'),
    )

    VERT_ALIGN_OPTION = (
        ('0', 'Center'),
        ('1', 'Top'),
        ('2', 'Bottom'),
    )

    HORZ_ALIGN_OPTION = (
        ('0', 'Center'),
        ('1', 'Left'),
        ('2', 'Right'),
    )

    descr = models.CharField(max_length=160, null=False, blank=False)
    pixels_width = models.IntegerField(null=False, blank=False, default=128)
    pixels_height = models.IntegerField(null=False, blank=False, default=32)
    text_color = models.CharField(max_length=1, choices=COLOR_OPTIONS,
                                  default='R')
    back_color = models.CharField(max_length=1, choices=COLOR_OPTIONS,
                                  default='K')
    in_mode = models.CharField(max_length=2, choices=MODE_OPTIONS, default='ML')
    out_mode = models.CharField(max_length=2, choices=MODE_OPTIONS,
                                default='ML')
    speed = models.CharField(max_length=1, choices=COLOR_OPTIONS, default='2')
    line_spacing = models.IntegerField(null=False, blank=False, default=1,
                                       validators=[MaxValueValidator(9),
                                                   MinValueValidator(0)])
    letter_size = models.CharField(max_length=1, choices=LETTER_SIZE,
                                   default='1')
    vertical_alignment = models.CharField(max_length=1,
                                          choices=VERT_ALIGN_OPTION, default=0)
    horizontal_alignment = models.CharField(max_length=1,
                                            choices=HORZ_ALIGN_OPTION,
                                            default=0)
    create_date = models.DateTimeField('create datetime', auto_now=False,
                                       auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)

    def __str__(self):
        return self.descr


class DisplayDevice(models.Model):
    reference_cd = models.CharField(max_length=20, null=False, blank=False)
    display = models.ForeignKey(DisplayType, on_delete=models.PROTECT)
    descr = models.CharField(max_length=160, null=False, blank=False)
    ip_address = models.GenericIPAddressField()
    port = models.IntegerField(null=False, blank=False, default=3001,
                               validators=[MaxValueValidator(65535),
                                           MinValueValidator(1)])
    entity = models.ForeignKey(MeasuredEntity, related_name='display_entity',
                               on_delete=models.CASCADE, null=True,
                               blank=True)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_compania = models.CharField(max_length=60)
    id_sede = models.CharField(max_length=60)
    id_planta = models.CharField(max_length=60)


class Period(models.Model):
    name = models.CharField(max_length=60)
    type = models.CharField(max_length=1, default='1')
    type_child = models.CharField(max_length=1, default='1')
    scale = models.IntegerField(null=True, blank=True)


class AggregateMethod(models.Model):
    name = models.CharField(max_length=60)
    descr = models.CharField(max_length=160, null=False, blank=False)
    method = models.CharField(max_length=160, null=False, blank=False)
    attribute = models.CharField(max_length=160, null=False, blank=False)
    create_date = models.DateTimeField('create datetime', auto_now=False,
                                       auto_now_add=True)
    period = models.ForeignKey(Period, on_delete=models.PROTECT)
