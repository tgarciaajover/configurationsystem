from django.contrib import admin
from django import forms
from django.forms import ModelForm
from django.db import transaction
from setup.models import SignalType
from setup.models import SignalUnit
from setup.models import Signal
from setup.models import DeviceType
from setup.models import IOSignalsDeviceType
from setup.models import MeasuredEntity
from setup.models import MonitoringDevice
from setup.models import MeasuredEntityBehavior
from setup.models import InputOutputPort
from setup.models import MeasuredEntityGroup
from setup.models import IdleReason
from setup.models import DisplayType
from setup.models import DisplayDevice
from setup.models import MeasuredEntityStateBehavior
from setup.models import MeasuredEntityTransitionState
from setup.models import MeasuredEntityScheduledEvent
from setup.models import MachineHostSystem
from setup.models import PlantHostSystem, IdleReasonHostSystem
from setup.models import ModBusInputOutputPort
from setup.models import MqttInputOutputPort
from setup.models import MqttMonitoringDevice
from setup.models import ModBusMonitoringDevice


from django.core.exceptions import ValidationError
import requests
import json
from setup.serializers import SignalUnitSerializer
from setup.serializers import SignalTypeSerializer
from setup.serializers import SignalSerializer
from setup.serializers import DeviceTypeSerializer
from setup.serializers import MonitoringDeviceSerializer
from setup.serializers import MeasuredEntitySerializer
from setup.serializers import DisplayTypeSerializer
from setup.serializers import DisplayDeviceSerializer
from setup.serializers import MeasuredEntityBehaviorSerializer
from setup.serializers import MeasuredEntityStateBehaviorSerializer
from setup.serializers import MeasuredEntityTransitionStateSerializer
from setup.serializers import MeasuredEntityScheduledEventSerializer
from setup.serializers import MachineHostSystemSerializer
from setup.serializers import PlantHostSystemSerializer

from canonical.models import Compania
from canonical.models import Sede
from canonical.models import Planta

from rest_framework.renderers import JSONRenderer
import setup.defaults as defaults
from django_ace import AceWidget

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from setup.models import Employee

from django.db.models.signals import pre_delete
from django.dispatch import receiver
from utils.advutils import get_logger

# Register your models here.

logger = get_logger('iot_settings_admin')


class SignalTypeForm(ModelForm):
    class Meta:
        model = SignalType
        fields = ['name', 'class_name', 'protocol']

    def getFromFileSystem(self, available_choices):
        try:
            f = open('workfile', 'r')
            for line in f:
                available_choices.append((line, line))
            f.close()
        except IOError:
            raise ValidationError("No class file definition was found")

    def formfield_for_choice_field(self, available_choices):
        # This method let the classes names in a temporal file in case
        # of proceeed to configure without being connected to the fog server.
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'TranslationClasses'
        try:
            r = requests.get(url)
            json = r.json()
            f = open('workfile', 'w')
            for className in json:
                className = className.split('.')[0]
                available_choices.append((className, className))
                f.write(className + '\n')
            f.close()
        except requests.exceptions.RequestException as e:
            logger.error(e)
            available_choices = self.getFromFileSystem(available_choices)

    def __init__(self, *args, **kwargs):
        super(SignalTypeForm, self).__init__(*args, **kwargs)
        available_choices = []
        self.formfield_for_choice_field(available_choices)
        self.fields['class_name'] = forms.ChoiceField(choices=available_choices)


class SignalTypeAdmin(admin.ModelAdmin):
    form = SignalTypeForm

    def save_model(self, request, obj, form, change):
        obj.save()
        serializer = SignalTypeSerializer(obj)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'SignalType' + '/' + str(obj.id)
        try:
            r = requests.put(url, data=content)
        except requests.exceptions.RequestException as e:
            logger.error(e)
            pass

    pass


@receiver(pre_delete, sender=SignalUnit)
def callback_delete_signal_unit(sender, instance, **kwargs):
    url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
    url = url + defaults.CONTEXT_ROOT + '/'
    url = url + 'SignalUnit' + '/' + str(instance.id)
    try:
        r = requests.delete(url)
    except requests.exceptions.RequestException as e:
        logger.error(e)
    pass


class SignalUnitAdmin(admin.ModelAdmin):
    list_display = ('descr', 'create_date')

    def save_model(self, request, obj, form, change):
        obj.save()
        serializer = SignalUnitSerializer(obj)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'SignalUnit' + '/' + str(obj.id)
        try:
            r = requests.put(url, data=content)
        except requests.exceptions.RequestException as e:
            logger.info(e)
            pass

    pass


@receiver(pre_delete, sender=Signal)
def callback_delete_signal(sender, instance, **kwargs):
    url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
    url = url + defaults.CONTEXT_ROOT + '/'
    url = url + 'Signal' + '/' + str(instance.id)
    try:
        r = requests.delete(url)
    except requests.exceptions.RequestException as e:
        logger.error(e)
    pass


class SignalAdmin(admin.ModelAdmin):
    list_display = ('descr', 'type')

    def save_model(self, request, obj, form, change):
        obj.save()
        serializer = SignalSerializer(obj)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'Signal' + '/' + str(obj.id)
        try:
            r = requests.put(url, data=content)
        except requests.exceptions.RequestException as e:
            logger.info(e)
            pass

    pass


class IOSignalsDeviceTypeInline(admin.TabularInline):
    model = IOSignalsDeviceType
    extra = 0
    pass


@receiver(pre_delete, sender=DeviceType)
def callback_delete_device_type(sender, instance, **kwargs):
    url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
    url = url + defaults.CONTEXT_ROOT + '/'
    url = url + 'DeviceType' + '/' + str(instance.id)
    try:
        r = requests.delete(url)
    except requests.exceptions.RequestException as e:
        logger.error(e)
    pass


class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ('descr', 'create_date')
    inlines = [IOSignalsDeviceTypeInline, ]

    def save_formset(self, request, form, formset, change):
        super(DeviceTypeAdmin, self).save_formset(request, form, formset, change)
        obj = formset.instance
        serializer = DeviceTypeSerializer(obj)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'DeviceType' + '/' + str(obj.id)
        try:
            r = requests.put(url, data=content)
        except requests.exceptions.RequestException as e:
            logger.info(e)
            pass

    pass


class BehaviorForm(forms.ModelForm):
    behavior_text = forms.CharField(
        widget=AceWidget(mode='behavior', width="700px", height="300px", showprintmargin=True))

    class Meta:
        model = MeasuredEntityBehavior
        fields = ['measure_entity', 'name', 'descr', 'behavior_text']


@receiver(pre_delete, sender=MeasuredEntityBehavior)
def callback_delete_measure_entity_behavior(sender, instance, **kwargs):
    try:
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MeasuredEntity' + '/' + str(instance.measure_entity_id) + '/Behavior/' + str(instance.id)
        r = requests.delete(url)
    except requests.exceptions.RequestException as e:
        logger.error(e)
    pass


class MeasuredEntityBehaviorAdmin(admin.ModelAdmin):
    model = MeasuredEntityBehavior
    form = BehaviorForm
    list_display = ('measure_entity', 'name', 'descr')
    list_filter = ('measure_entity',)

    def get_actions(self, request):
        """
        It is not possible to perfom the delete action for this model.
        If we let this functionality to operate, then we are not checking
        that a behavior is being used in a transformation.
        """
        actions = super(MeasuredEntityBehaviorAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']

        return actions

    def save_model(self, request, obj, form, change):
        obj.save()
        serializer = MeasuredEntityBehaviorSerializer(obj)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MeasuredEntity' + '/' + str(obj.measure_entity_id) + '/Behavior/' + str(obj.id)
        try:
            r = requests.put(url, data=content)
        except requests.exceptions.RequestException as e:
            logger.info(e)
            pass

    pass


@receiver(pre_delete, sender=MachineHostSystem)
def callback_delete_machine(sender, instance, **kwargs):
    url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
    url = url + defaults.CONTEXT_ROOT + '/'
    url = url + 'MeasuredEntity' + '/' + str(instance.id)
    try:
        r = requests.delete(url)
    except requests.exceptions.RequestException as e:
        logger.error(e)
    pass


class MachineHostSystemAdmin(admin.ModelAdmin):
    list_display = ('code', 'descr')

    def save_model(self, request, obj, form, change):
        obj.save()
        serializer = MachineHostSystemSerializer(obj)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MeasuredEntity' + '/' + str(obj.id)
        try:
            r = requests.put(url, data=content)
        except requests.exceptions.RequestException as e:
            logger.info(e)
            pass

    pass


@receiver(pre_delete, sender=PlantHostSystem)
def callback_delete_plant(sender, instance, **kwargs):
    url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
    url = url + defaults.CONTEXT_ROOT + '/'
    url = url + 'MeasuredEntity' + '/' + str(instance.id)
    try:
        r = requests.delete(url)
    except requests.exceptions.RequestException as e:
        logger.error(e)
    pass


class PlantHostSystemAdmin(admin.ModelAdmin):
    list_display = ('code', 'descr')

    def save_model(self, request, obj, form, change):
        obj.save()
        serializer = PlantHostSystemSerializer(obj)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MeasuredEntity' + '/' + str(obj.id)
        try:
            r = requests.put(url, data=content)
        except requests.exceptions.RequestException as e:
            logger.info(e)
            pass

    pass


@receiver(pre_delete, sender=MeasuredEntityStateBehavior)
def callback_delete_measured_entity_state_behavior(sender, instance, **kwargs):
    url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
    url = url + defaults.CONTEXT_ROOT + '/'
    url = url + 'MeasuredEntity' + '/' + str(instance.measure_entity_id) + '/StateBehavior/' + str(instance.id)
    try:
        r = requests.delete(url)
    except requests.exceptions.RequestException as e:
        logger.error(e)
    pass


class BehaviorStateForm(forms.ModelForm):
    behavior_text = forms.CharField(
        widget=AceWidget(mode='behavior', width="700px", height="300px", showprintmargin=True))

    class Meta:
        model = MeasuredEntityStateBehavior
        fields = ['measure_entity', 'state_behavior_type', 'descr', 'behavior_text']


class MeasuredEntityStateBehaviorAdmin(admin.ModelAdmin):
    model = MeasuredEntityStateBehavior
    form = BehaviorStateForm

    def save_model(self, request, obj, form, change):
        obj.save()
        serializer = MeasuredEntityStateBehaviorSerializer(obj)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MeasuredEntity' + '/' + str(obj.measure_entity_id) + '/StateBehavior/' + str(obj.id)
        try:
            r = requests.put(url, data=content)
        except requests.exceptions.RequestException as e:
            logger.info(e)
            pass


@receiver(pre_delete, sender=MeasuredEntityScheduledEvent)
def callback_delete_measured_entity_schedule_event(sender, instance, **kwargs):
    url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
    url = url + defaults.CONTEXT_ROOT + '/'
    url = url + 'MeasuredEntity' + '/' + str(instance.measure_entity_id) + '/ScheduledEvent/' + str(instance.id)
    try:
        r = requests.delete(url)
    except requests.exceptions.RequestException as e:
        logger.error(e)
    pass


class ScheduleEventForm(forms.ModelForm):
    class Meta:
        model = MeasuredEntityScheduledEvent
        fields = ['measure_entity', 'scheduled_event_type', 'descr', 'recurrences', 'day_time']


class MeasuredEntityScheduledEventAdmin(admin.ModelAdmin):
    model = MeasuredEntityScheduledEvent
    form = ScheduleEventForm

    def save_model(self, request, obj, form, change):
        obj.save()
        serializer = MeasuredEntityScheduledEventSerializer(obj)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MeasuredEntity' + '/' + str(obj.measure_entity_id) + '/ScheduledEvent/' + str(obj.id)
        try:
            r = requests.put(url, data=content)
        except requests.exceptions.RequestException as e:
            logger.error(e)
            pass


@receiver(pre_delete, sender=MonitoringDevice)
def callback_delete_monitoring_device(sender, instance, **kwargs):
    url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
    url = url + defaults.CONTEXT_ROOT + '/'
    url = url + 'MonitoringDevice' + '/' + str(instance.id)
    try:
        r = requests.delete(url)
    except requests.exceptions.RequestException as e:
        logger.error(e)
    pass


class ModBusInputOutputPortForm(forms.ModelForm):
    transformation_text = forms.CharField(
        widget=AceWidget(mode='transform', width="700px", height="300px", showprintmargin=True))

    class Meta:
        model = ModBusInputOutputPort
        fields = ['port_label', 'signal_type', 'refresh_time_ms',
                  'measured_entity', 'port', 'unit_id', 'offset', 'nbr_read',
                  'object_type', 'access', 'transformation_text']

class ModBusInputOutputPortInline(admin.StackedInline):
    model = ModBusInputOutputPort
    form = ModBusInputOutputPortForm
    extra = 0
    pass


class MqttInputOutputPortForm(forms.ModelForm):
    transformation_text = forms.CharField(
        widget=AceWidget(mode='transform', width="700px", height="300px", showprintmargin=True))

    class Meta:
        model = MqttInputOutputPort
        fields = ['port_label', 'signal_type', 'refresh_time_ms',
                  'measured_entity', 'topic_name', 'transformation_text']


class MqttInputOutputPortInline(admin.StackedInline):
    model = MqttInputOutputPort
    form = MqttInputOutputPortForm
    extra = 0
    pass


class MqttMonitoringDeviceAdmin(admin.ModelAdmin):
    list_display = ('descr', 'mac_address', 'serial')
    inlines = [MqttInputOutputPortInline, ]

    def save_formset(self, request, form, formset, change):
        with transaction.atomic():
            super(MqttMonitoringDeviceAdmin, self).save_formset(request, form, formset, change)

        obj = formset.instance
        serializer = MonitoringDeviceSerializer(obj)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MonitoringDevice' + '/' + str(obj.id)
        try:
            r = requests.put(url, data=content)
        except requests.exceptions.RequestException as e:
            logger.info(e)
            pass

    pass


class ModBusMonitoringDeviceAdmin(admin.ModelAdmin):
    list_display = ('descr', 'mac_address', 'serial')
    inlines = [ModBusInputOutputPortInline, ]

    def save_formset(self, request, form, formset, change):
        with transaction.atomic():
            super(ModBusMonitoringDeviceAdmin, self).save_formset(request, form, formset, change)

        obj = formset.instance
        serializer = MonitoringDeviceSerializer(obj)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MonitoringDevice' + '/' + str(obj.id)
        try:
            r = requests.put(url, data=content)
        except requests.exceptions.RequestException as e:
            logger.info(e)
            pass

    pass


class MeasuredEntityGroupAdmin(admin.ModelAdmin):
    list_display = ('descr',)
    pass


class IdleReasonAdmin(admin.ModelAdmin):
    list_display = ('descr', 'group_cd', 'classification', 'down')
    pass


@receiver(pre_delete, sender=MeasuredEntityTransitionState)
def callback_delete_measured_entity_transition_state(sender, instance, **kwargs):
    url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
    url = url + defaults.CONTEXT_ROOT + '/'
    url = url + 'MeasuredEntity' + '/' + str(instance.measure_entity_id) + '/StateTransition/' + str(instance.id)
    try:
        r = requests.delete(url)
    except requests.exceptions.RequestException as e:
        logger.error(e)
    pass


class MeasuredStateTransitionForm(forms.ModelForm):
    class Meta:
        model = MeasuredEntityTransitionState
        fields = ['measure_entity', 'state_from', 'reason_code', 'behavior']


class MeasuredStateTransitionAdmin(admin.ModelAdmin):
    model = MeasuredEntityTransitionState
    form = MeasuredStateTransitionForm
    list_display = ('measure_entity', 'state_from', 'reason_code', 'behavior')
    list_filter = ('measure_entity',)

    def save_model(self, request, obj, form, change):
        obj.save()
        serializer = MeasuredEntityTransitionStateSerializer(obj)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MeasuredEntity' + '/' + str(obj.measure_entity_id) + '/StateTransition/' + str(obj.id)
        try:
            print(content)
            r = requests.put(url, data=content)
        except requests.exceptions.RequestException as e:
            logger.info(e)
            pass


class DisplayTypeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('descr', 'vertical_alignment', 'horizontal_alignment', 'letter_size')
        }),
        ('Colors', {
            'fields': ('text_color', 'back_color')
        }),
        ('Placement', {
            'fields': ('pixels_width', 'pixels_height', 'in_mode', 'out_mode', 'speed')
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.save()
        serializer = DisplayTypeSerializer(obj)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'DisplayType' + '/' + str(obj.id)
        try:
            r = requests.put(url, data=content)
        except requests.exceptions.RequestException as e:
            logger.info(e)
            pass


class DisplayDeviceAdmin(admin.ModelAdmin):
    list_display = ('descr', 'display', 'ip_address', 'port')

    def save_model(self, request, obj, form, change):
        obj.save()
        serializer = DisplayDeviceSerializer(obj)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'DisplayDevice' + '/' + str(obj.id)
        try:
            r = requests.put(url, data=content)
        except requests.exceptions.RequestException as e:
            logger.info(e)
            pass


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class EmployeeInLineForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

    verbose_name_plural = 'employee'
    can_delete = False

    def compania_for_choice_field(self, available_choices):
        all_companies = Compania.objects.all()
        for compania in all_companies:
            available_choices.append((compania.id, compania.descr))

    def sede_for_choice_field(self, available_choices):
        all_sedes = Sede.objects.all()
        for sede in all_sedes:
            available_choices.append((sede.id, sede.descr))

    def planta_for_choice_fields(self, available_choices):
        all_plantas = Planta.objects.all()
        for planta in all_plantas:
            available_choices.append((planta.id, planta.descr))

    def __init__(self, *args, **kwargs):
        super(EmployeeInLineForm, self).__init__(*args, **kwargs)

        compania_available_choices = []
        self.compania_for_choice_field(compania_available_choices)
        self.fields['id_compania'] = forms.ChoiceField(choices=compania_available_choices)

        sede_available_choices = []
        self.sede_for_choice_field(sede_available_choices)
        self.fields['id_sede'] = forms.ChoiceField(choices=sede_available_choices)

        planta_available_choices = []
        self.planta_for_choice_fields(planta_available_choices)
        self.fields['id_planta'] = forms.ChoiceField(choices=planta_available_choices)


class EmployeeInLineAdmin(admin.StackedInline):
    model = Employee
    form = EmployeeInLineForm


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (EmployeeInLineAdmin,)


admin.site.register(SignalType, SignalTypeAdmin)
admin.site.register(SignalUnit, SignalUnitAdmin)
admin.site.register(Signal, SignalAdmin)
admin.site.register(DeviceType, DeviceTypeAdmin)
admin.site.register(MqttMonitoringDevice, MqttMonitoringDeviceAdmin)
admin.site.register(ModBusMonitoringDevice, ModBusMonitoringDeviceAdmin)
admin.site.register(MeasuredEntityGroup, MeasuredEntityGroupAdmin)
admin.site.register(MachineHostSystem, MachineHostSystemAdmin)
admin.site.register(PlantHostSystem, PlantHostSystemAdmin)
admin.site.register(MeasuredEntityBehavior, MeasuredEntityBehaviorAdmin)
admin.site.register(MeasuredEntityScheduledEvent, MeasuredEntityScheduledEventAdmin)
admin.site.register(MeasuredEntityStateBehavior, MeasuredEntityStateBehaviorAdmin)
admin.site.register(MeasuredEntityTransitionState, MeasuredStateTransitionAdmin)
admin.site.register(IdleReason, IdleReasonAdmin)
admin.site.register(DisplayType, DisplayTypeAdmin)
admin.site.register(DisplayDevice, DisplayDeviceAdmin)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(IdleReasonHostSystem)
