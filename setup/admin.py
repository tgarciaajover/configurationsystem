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
import requests
from setup.serializers import SignalUnitSerializer
from setup.serializers import SignalTypeSerializer
from setup.serializers import SignalSerializer
from setup.serializers import DeviceTypeSerializer
from setup.serializers import MonitoringDeviceSerializer
from setup.serializers import MeasuredEntitySerializer
from setup.serializers import DisplayTypeSerializer
from setup.serializers import DisplayDeviceSerializer

import logging
import os
import logging.handlers

from rest_framework.renderers import JSONRenderer
import setup.defaults as defaults
from django_ace import AceWidget

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
        fields = ['name', 'class_name']

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
        fields = ['name','descr', 'behavior_text']

class BehaviorInline(admin.StackedInline):
    model = MeasuredEntityBehavior
    form = BehaviorForm
    extra = 0 
    pass

class MeasuredEntityAdmin(admin.ModelAdmin):
    list_display = ('code', 'descr')
    inlines = [
        BehaviorInline,
      ]

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

admin.site.register(SignalType, SignalTypeAdmin)
admin.site.register(SignalUnit, SignalUnitAdmin)
admin.site.register(Signal, SignalAdmin)
admin.site.register(DeviceType, DeviceTypeAdmin)
admin.site.register(MeasuredEntity, MeasuredEntityAdmin)
admin.site.register(MonitoringDevice, MonitoringDeviceAdmin)
admin.site.register(MeasuredEntityGroup, MeasuredEntityGroupAdmin)
admin.site.register(IdleReason,IdleReasonAdmin)
admin.site.register(DisplayType, DisplayTypeAdmin)
admin.site.register(DisplayDevice, DisplayDeviceAdmin)
