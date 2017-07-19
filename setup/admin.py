from django.contrib import admin
from django import forms
from django.forms import ModelForm
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

import requests
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

from canonical.models import Compania
from canonical.models import Sede
from canonical.models import Planta

import logging
import os
import logging.handlers

from rest_framework.renderers import JSONRenderer
import setup.defaults as defaults
from django_ace import AceWidget

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from setup.models import Employee

# Register your models here.

# Get an instance of a logger
LOG_FILENAME = 'iotsettings.log'

# Check if log exists and should therefore be rolled
needRoll = os.path.isfile(LOG_FILENAME)

logger = logging.getLogger('admin')

fh = logging.handlers.RotatingFileHandler(LOG_FILENAME, backupCount=5)
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

# This is a stale log, so roll it
if needRoll:
	# Roll over on application start
    logger.handlers[0].doRollover()

class SignalTypeForm(ModelForm):
    class Meta:
        model = SignalType
        fields = ['name', 'class_name', 'protocol']

    def getFromFileSystem(self, available_choices):
       f = open('workfile', 'r')
       for line in f:
          available_choices.append((line, line))
       f.close()       
 
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
           logger.info(e)
           available_choices = self.getFromFileSystem(available_choices)

    def __init__(self, *args, **kwargs):
        super(SignalTypeForm, self).__init__(*args, **kwargs)
        available_choices = []
        self.formfield_for_choice_field(available_choices)
        self.fields['class_name'] = forms.ChoiceField(choices=available_choices)

class SignalTypeAdmin(admin.ModelAdmin):
    form = SignalTypeForm    

    def save_model(self,request,obj,form,change):
       obj.save()
       serializer = SignalTypeSerializer(obj)
       content = JSONRenderer().render(serializer.data)
       url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
       url = url + defaults.CONTEXT_ROOT + '/'
       url = url + 'SignalType' + '/' + str(obj.id)
       try:
           r = requests.put(url, data = content)
       except requests.exceptions.RequestException as e:
           logger.info(e)
           pass
   
    pass
 
class SignalUnitAdmin(admin.ModelAdmin):
    list_display = ('descr','create_date')

    def save_model(self, request, obj, form, change):
        obj.save()
        serializer = SignalUnitSerializer(obj)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'SignalUnit' + '/' + str(obj.id)
        try:
            r = requests.put(url, data = content)
        except requests.exceptions.RequestException as e:
            logger.info(e)
            pass
    
    pass

class SignalAdmin(admin.ModelAdmin):
    list_display = ('descr','type')
  
    def save_model(self,request, obj, form, change):
        obj.save()
        serializer = SignalSerializer(obj)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'Signal' + '/' + str(obj.id)
        try:
            r = requests.put(url, data = content)
        except requests.exceptions.RequestException as e:
           logger.info(e)
           pass
  
    pass


class IOSignalsDeviceTypeInline(admin.TabularInline):
    model = IOSignalsDeviceType
    extra = 0 
    pass

class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ('descr','create_date')
    inlines = [ IOSignalsDeviceTypeInline, ]

    def save_model(self,request, obj, form, change):
        obj.save()
        serializer = DeviceTypeSerializer(obj)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'DeviceType' + '/' + str(obj.id)
        try:
            r = requests.put(url, data = content)
        except requests.exceptions.RequestException as e:
           logger.info(e)
           pass

    pass

class BehaviorForm(forms.ModelForm):
    behavior_text = forms.CharField(widget=AceWidget(mode='behavior', width="700px", height="300px", showprintmargin=True))
    class Meta:
        model = MeasuredEntityBehavior
        fields = ['measure_entity','name','descr', 'behavior_text']

class MeasuredEntityBehaviorAdmin(admin.ModelAdmin):
    model = MeasuredEntityBehavior
    form = BehaviorForm
    list_display = ('measure_entity', 'name', 'descr')
    list_filter = ('measure_entity',)

    def save_model(self,request, obj, form, change):
        obj.save()
        serializer = MeasuredEntityBehaviorSerializer(obj)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MeasuredEntity' + '/' + str(obj.measure_entity_id) + '/Behavior/' + str(obj.name) 
        try:
            r = requests.put(url, data = content)
        except requests.exceptions.RequestException as e:
           logger.info(e)
           pass

    pass


class MeasuredEntityAdmin(admin.ModelAdmin):
    list_display = ('code', 'descr')

    def save_model(self,request, obj, form, change):
        obj.save()
        serializer = MeasuredEntitySerializer(obj)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MeasuredEntity' + '/' + str(obj.id)
        try:
            r = requests.put(url, data = content)
        except requests.exceptions.RequestException as e:
           logger.info(e)
           pass
    pass

class BehaviorStateForm(forms.ModelForm):
    behavior_text = forms.CharField(widget=AceWidget(mode='behavior', width="700px", height="300px", showprintmargin=True))
    class Meta:
        model = MeasuredEntityStateBehavior
        fields = ['measure_entity','state_behavior_type','descr', 'behavior_text']


class MeauredEntityStateBehaviorAdmin(admin.ModelAdmin):
    model = MeasuredEntityStateBehavior
    form = BehaviorStateForm

    def save_model(self,request, obj, form, change):
        obj.save()
        serializer = MeasuredEntityStateBehaviorSerializer(obj)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MeasuredEntity' + '/' + str(obj.measure_entity_id) + '/StateBehavior/' + str(obj.id) 
        try:
            r = requests.put(url, data = content)
        except requests.exceptions.RequestException as e:
           logger.info(e)
           pass

class InputOutputPortForm(forms.ModelForm):
    transformation_text = forms.CharField(widget=AceWidget(mode='transform', width="700px", height="300px", showprintmargin=True))
    class Meta:
        model = InputOutputPort
        fields = ['port_label', 'signal_type', 'measured_entity', 'transformation_text']  

class InputOutputPortInline(admin.StackedInline):
    model = InputOutputPort
    form = InputOutputPortForm
    extra=0

    pass

class MonitoringDeviceAdmin(admin.ModelAdmin):
    list_display = ('descr', 'mac_address','serial')
    inlines = [ InputOutputPortInline, ]

    def save_model(self,request, obj, form, change):
        obj.save()
        serializer = MonitoringDeviceSerializer(obj)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MonitoringDevice' + '/' + str(obj.id)
        try:
            r = requests.put(url, data = content)
        except requests.exceptions.RequestException as e:
           logger.info(e)
           pass

    pass

class MeasuredEntityGroupAdmin(admin.ModelAdmin):
    list_display = ('descr',)
    pass

class IdleReasonAdmin(admin.ModelAdmin):
    list_display = ('descr','group_cd', 'classification','down')
    pass

class MeasuredStateTransitionForm(forms.ModelForm):
    class Meta:
        model = MeasuredEntityTransitionState
        fields = ['measure_entity','state_from','reason_code', 'behavior']

class MeasuredStateTransitionAdmin(admin.ModelAdmin):
    model = MeasuredEntityTransitionState
    form = MeasuredStateTransitionForm
    list_display = ('measure_entity', 'state_from', 'reason_code', 'behavior')
    list_filter = ('measure_entity',)

    def save_model(self,request, obj, form, change):
        obj.save()
        serializer = MeasuredEntityTransitionStateSerializer(obj)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MeasuredEntity' + '/' + str(obj.measure_entity_id) + '/StateTransition/' + str(obj.id) 
        try:
            print (content)
            r = requests.put(url, data = content)
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

    def save_model(self,request, obj, form, change):
        obj.save()
        serializer = DisplayTypeSerializer(obj)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'DisplayType' + '/' + str(obj.id)
        try:
            r = requests.put(url, data = content)
        except requests.exceptions.RequestException as e:
           logger.info(e)
           pass

class DisplayDeviceAdmin(admin.ModelAdmin):
    list_display =  ('descr', 'display', 'ip_address', 'port')

    def save_model(self,request, obj, form, change):
        obj.save()
        serializer = DisplayDeviceSerializer(obj)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'DisplayDevice' + '/' + str(obj.id)
        try:
            r = requests.put(url, data = content)
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
     inlines = (EmployeeInLineAdmin, )

admin.site.register(SignalType, SignalTypeAdmin)
admin.site.register(SignalUnit, SignalUnitAdmin)
admin.site.register(Signal, SignalAdmin)
admin.site.register(DeviceType, DeviceTypeAdmin)
admin.site.register(MeasuredEntity, MeasuredEntityAdmin)
admin.site.register(MeasuredEntityStateBehavior, MeauredEntityStateBehaviorAdmin)
admin.site.register(MeasuredEntityBehavior, MeasuredEntityBehaviorAdmin)
admin.site.register(MonitoringDevice, MonitoringDeviceAdmin)
admin.site.register(MeasuredEntityGroup, MeasuredEntityGroupAdmin)
admin.site.register(IdleReason,IdleReasonAdmin)
admin.site.register(MeasuredEntityTransitionState, MeasuredStateTransitionAdmin)
admin.site.register(DisplayType, DisplayTypeAdmin)
admin.site.register(DisplayDevice, DisplayDeviceAdmin)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
