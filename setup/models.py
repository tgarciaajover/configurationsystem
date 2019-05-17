from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
import setup.defaults as defaults
from simple_history.models import HistoricalRecords
from django.utils.six import python_2_unicode_compatible
import common.models as common
import xml.etree.ElementTree as ET
import requests
from django.contrib.auth.models import User
from recurrence.fields import RecurrenceField
from macaddress.fields import MACAddressField
from utils.advutils import get_logger

from graph_types.models import GraphType

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
    tiempo_refresco = models.IntegerField(default=5)

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


class Operator(common.AuditedModel):
    IDENTIFICATION_TYPE = (
        ('C', 'Cedula'),
        ('P', 'Pasaporte',),
        ('E', 'Cedula de Extranjeria'),
        ('T', 'Tarjeta de Identidad'),
        ('U', 'Registro Civil'),
        ('D', 'Carnet Diplomatico'),
        ('O', 'TI2')
    )
    first_name = models.CharField(max_length=120)
    second_name = models.CharField(max_length=120, null=True, blank=True)
    other_names = models.CharField(max_length=120, null=True, blank=True)
    surname = models.CharField(max_length=120)
    second_last_name = models.CharField(max_length=120, null=True, blank=True)
    other_surnames = models.CharField(max_length=120, null=True, blank=True)
    email = models.EmailField(max_length=200)
    address = models.CharField(max_length=300, null=True)
    phone = models.CharField(max_length=150, blank=True)
    identification_type = models.CharField(max_length=2, choices=IDENTIFICATION_TYPE, null=True, blank=True)
    identification = models.CharField(max_length=20, null=True, blank=True)
    user = models.OneToOneField(User, related_name='person')

    active_account = models.BooleanField(default=True)

    history = HistoricalRecords()

    class Meta:
        unique_together = ('identification_type', 'identification', 'user')

    def __str__(self):
        return "{} {} Identification: {}".format(self.first_name, self.surname, self.identification)


class ThirdParty(common.AuditedModel):
    visible_name = models.CharField(max_length=200)

    history = HistoricalRecords()

    def __str__(self):
        return self.visible_name


class Phone(common.AuditedModel):
    ROL_PHONE = (
        ('M', 'Main'),
        ('S', 'Secondary'),
    )
    third_part = models.ForeignKey(ThirdParty, on_delete=models.CASCADE)
    country_code = models.CharField(max_length=2)
    city_code = models.CharField(max_length=1)
    number = models.CharField(max_length=10)
    rol = models.CharField(max_length=2, choices=ROL_PHONE, null=True, blank=True)

    history = HistoricalRecords()


class Email(common.AuditedModel, common.ValidModel):
    ROL_EMAIL = (
        ('M', 'Main'),
        ('S', 'Secondary'),
    )
    third_party = models.ForeignKey(ThirdParty, on_delete=models.CASCADE)
    email = models.EmailField(max_length=200)
    rol = models.CharField(max_length=2, choices=ROL_EMAIL, null=True, blank=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "Emails"


@python_2_unicode_compatible
class Department(models.Model):
    department_dane_code = models.CharField(max_length=2)
    name = models.CharField(max_length=60, null=True)

    class Meta:
        """Meta."""

        verbose_name = "Departament"
        verbose_name_plural = "Departaments"

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Municipality(models.Model):
    municipality_dane_code = models.CharField(max_length=5, null=True)
    departament = models.ForeignKey(Department, related_name='departament', on_delete=models.PROTECT)
    name = models.CharField(max_length=60, null=True)

    class Meta:
        """Meta."""

        verbose_name = "Municipality"
        verbose_name_plural = "Municipalities"

    def __str__(self):
        return self.name


class UrbanDirectionColombia(models.Model):
    VIA_TYPE = (
        ('AU', 'Freeway'),
        ('AV', 'Avenue'),
        ('AC', 'Avenue Street'),
        ('AK', 'Avenue Carrera'),
        ('BL', 'Boulevard'),
        ('CL', 'Street'),
        ('KR', 'Carrera'),
        ('CT', 'Highway'),
        ('CQ', 'Peripheral'),
        ('CV', 'Encircle'),
        ('DG', 'Diagonal'),
        ('PJ', 'Passage'),
        ('PS', 'Walk'),
        ('PT', 'Pedestrian'),
        ('TV', 'Transversal'),
        ('TC', 'Trunk'),
        ('VT', 'Variant'),
        ('VI', 'Vía')
    )

    QUADRANT = (
        ('S', 'South'),
        ('N', 'North'),
        ('E', 'East'),
        ('W', 'West')
    )

    PREFIX = (
        ('B', 'BIS'),
    )

    ADDRESS_ADD_ON = (
        ('AD', 'ADMINISTRATION'),
        ('AG', 'AGRUPATION'),
        ('AL', 'LOFT'),
        ('AP', 'APARTAMENT'),
        ('BR', 'NEIGHBORHOOD'),
        ('BQ', 'BLOCK'),
        ('BG', 'CELLAR'),
        ('CS', 'HOUSE'),
        ('CU', 'CELL'),
        ('CE', 'MALL'),
        ('CD', 'CITADEL'),
        ('CO', 'RESIDENTIAL'),
        ('CN', 'CONSULTING_ROOM'),
        ('DP', 'DEPOSIT'),
        ('DS', 'BASEMENT_DEPOSIT'),
        ('ED', 'BUILDING'),
        ('EN', 'ENTRANCE'),
        ('EQ', 'CORNER'),
        ('ES', 'STATION'),
        ('ET', 'STAGE'),
        ('EX', 'EXTERIOR'),
        ('FI', 'ESTATE'),
        ('GA', 'GARAGE'),
        ('GS', 'BASEMENT_GARAGE'),
        ('IN', 'INTERIOR'),
        ('KM', 'KILOMETER'),
        ('LC', 'LOCAL'),
        ('LM', 'MEZZANINE_LOCAL'),
        ('LT', 'LOT'),
        ('MZ', 'APPlE'),
        ('MN', 'MEZZANINE'),
        ('MD', 'MODULE'),
        ('OF', 'OFFICE'),
        ('PQ', 'PARK'),
        ('PA', 'PARKING_LOT'),
        ('PN', 'PENT_HOUSE'),
        ('PI', 'FLOOR'),
        ('PL', 'LEVEL'),
        ('PR', 'PORTERIA'),
        ('PD', 'PREDIO'),
        ('PU', 'POST'),
        ('RP', 'ROUND POINT'),
        ('SC', 'SECTOR'),
        ('SS', 'SEMISOTANO'),
        ('SO', 'BASEMENT'),
        ('ST', 'SUITE'),
        ('SM', 'SUPERMANZANA'),
        ('TZ', 'TERRACE'),
        ('TO', 'TOWER'),
        ('UN', 'UNIT'),
        ('UL', 'RESIDENCIAL_UNIT'),
        ('UR', 'URBANIZATION'),
        ('ZN', 'ZONE')
    )

    ADDRESS_TYPE = (
        ('N', 'National'),
        ('E', 'Exterior'),
    )

    address_type = models.CharField(max_length=2, choices=ADDRESS_TYPE, null=True, blank=True, default='N')
    via_type = models.CharField(max_length=2, choices=VIA_TYPE, help_text="Tipe of via, ej: Avenida")
    main_via = models.CharField('Número/Nombre', max_length=30, help_text="Number or name common main via, ej: Esperanza")
    letter_main_via = models.CharField(max_length=3, null=True, blank=True, help_text="Letters assosiated to the main via")
    quadrant_main_via = models.CharField(max_length=1, choices=QUADRANT, null=True, blank=True, help_text="(North, South, East, West)")
    generator_via = models.CharField(max_length=30, help_text="Number or common generator via name, eg: 62")
    letter_generator_via = models.CharField(max_length=3, null=True, blank=True, help_text="Letters assosiated to the generator via")
    prefix_generator_via = models.CharField("Prefix", max_length=1, choices=PREFIX, null=True, blank=True, help_text="Via generator sufix, eg: Bis")
    prefix_letter_generator_via = models.CharField(max_length=3, null=True, blank=True, help_text="Letter that accompanies the suffix")
    number_plate = models.CharField(max_length=2, help_text="Plate, eg: 49")
    quadrant_generator_via = models.CharField("Quadrant", max_length=1, choices=QUADRANT, null=True, blank=True, help_text="(North, South, East, West)")
    complement = models.CharField(max_length=2, choices=ADDRESS_ADD_ON, null=True, blank=True)
    departament = models.ForeignKey(Department)
    municipality = models.ForeignKey(Municipality)

    class Meta:
        verbose_name_plural = "Addresses in Colombia"

    def __unicode__(self):
        return "{} {} {} {} {} {} {} {} {} {} {}".format(
            self.via_type or "",
            self.main_via or "",
            self.letter_main_via or "",
            self.quadrant_main_via or "",
            self.generator_via or "",
            self.letter_generator_via or "",
            self.prefix_generator_via or "",
            self.prefix_letter_generator_via or "",
            self.number_plate or "",
            self.quadrant_generator_via or "",
            self.complement or ""
        )


class MeasuredEntityOperator(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    measured_entity = models.ForeignKey(MeasuredEntity, on_delete=models.CASCADE)


class MeasuringEntityStatusInterval(models.Model):
    id_owner = models.IntegerField()
    owner_type = models.IntegerField()
    datetime_to = models.DateTimeField()
    datetime_from = models.DateTimeField()
    status = models.CharField(max_length=300)
    related_object = models.IntegerField(null=True, blank=True)
    related_object_type = models.IntegerField(null=True, blank=True)
    reason_code = models.CharField(max_length=300, null=True, blank=True)
    executed_object_canonical = models.CharField(max_length=300, null=True, blank=True)
    production_rate = models.DecimalField(max_digits=19, decimal_places=10, null=True, blank=True)
    conversion_1 = models.DecimalField(max_digits=19, decimal_places=10, null=True, blank=True)
    conversion_2 = models.DecimalField(max_digits=19, decimal_places=10, null=True, blank=True)
    actual_production_rate = models.DecimalField(max_digits=19, decimal_places=10, null=True, blank=True)
    qty_defective = models.DecimalField(max_digits=19, decimal_places=10, null=True, blank=True)

    class Meta:
        db_table = 'measuringentitystatusinterval'


class MeasuredAttributeValue(models.Model):
    id_owner = models.IntegerField()
    owner_type = models.IntegerField()
    attribute_name = models.CharField(max_length=300)
    value_decimal = models.DecimalField(max_digits=19, decimal_places=10, null=True, blank=True)
    value_datetime = models.DateTimeField(null=True, blank=True)
    value_string = models.CharField(max_length=300, null=True, blank=True)
    value_int = models.IntegerField(null=True, blank=True)
    value_boolean = models.BooleanField(default=False)
    value_date = models.DateField(null=True, blank=True)
    value_time = models.TimeField(null=True, blank=True)
    timestamp = models.DateTimeField()

    class Meta:
        db_table = 'measuredattributevalue'