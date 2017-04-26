from django.contrib import admin
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
from setup.models import GroupIdleReason
from setup.models import IdleReason
import requests
from setup.serializers import SignalUnitSerializer
from setup.serializers import SignalTypeSerializer
from setup.serializers import SignalSerializer
from setup.serializers import DeviceTypeSerializer
from setup.serializers import MonitoringDeviceSerializer
from rest_framework.renderers import JSONRenderer
import setup.defaults as defaults

# Register your models here.

class SignalTypeAdmin(admin.ModelAdmin):
    list_display = ('name','class_name')

    def save_model(self,request,obj,form,change):
       obj.save()
       serializer = SignalTypeSerializer(obj)
       content = JSONRenderer().render(serializer.data)
       url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
       url = url + defaults.CONTEXT_ROOT + '/'
       url = url + 'SignalType' + '/' + str(obj.id)
       r = requests.put(url, data = content)
       # TODO: exception handling.
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
        r = requests.put(url, data = content)
        # TODO: exception handling.
    pass

class SignalAdmin(admin.ModelAdmin):
    list_display = ('descr','type')
  
    def save_model(self,request, obj, form, change):
        obj.save()
        serializer = SignalSerializer(obj)
        content = JSONRenderer().render(serializer.data)
        print(content)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'Signal' + '/' + str(obj.id)
        r = requests.put(url, data = content)
        # TODO: exception handling.

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
        print(content)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'DeviceType' + '/' + str(obj.id)
        r = requests.put(url, data = content)
        # TODO: exception handling.

    pass

class BehaviorInline(admin.StackedInline):
    model = MeasuredEntityBehavior

class MeasuredEntityAdmin(admin.ModelAdmin):
    list_display = ('code', 'descr')
    inlines = [
        BehaviorInline,
      ]
    pass

class InputOutputPortInline(admin.StackedInline):
    model = InputOutputPort
    fieldsets = (
	(None, { 'fields': ('port_label', 'signal_type', 'measured_entity'), }),
        ('Program', {'fields': ('transformation_text',), }),
    )
    extra=0
    pass

class MonitoringDeviceAdmin(admin.ModelAdmin):
    list_display = ('descr', 'mac_address','serial')
    inlines = [ InputOutputPortInline, ]
    pass

class MeasuredEntityGroupAdmin(admin.ModelAdmin):
    list_display = ('descr',)
    pass

class GroupIdleReasonAdmin(admin.ModelAdmin):
    list_display = ('descr',)
    pass

class IdleReasonAdmin(admin.ModelAdmin):
    list_display = ('descr','group', 'classification','down')
    pass

admin.site.register(SignalType, SignalTypeAdmin)
admin.site.register(SignalUnit, SignalUnitAdmin)
admin.site.register(Signal, SignalAdmin)
admin.site.register(DeviceType, DeviceTypeAdmin)
admin.site.register(MeasuredEntity, MeasuredEntityAdmin)
admin.site.register(MonitoringDevice, MonitoringDeviceAdmin)
admin.site.register(MeasuredEntityGroup, MeasuredEntityGroupAdmin)
admin.site.register(GroupIdleReason, GroupIdleReasonAdmin)
admin.site.register(IdleReason,IdleReasonAdmin)
