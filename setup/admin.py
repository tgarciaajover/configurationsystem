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

# Register your models here.

class SignalTypeAdmin(admin.ModelAdmin):
    list_display = ('name','class_name')
    pass

class SignalUnitAdmin(admin.ModelAdmin):
    list_display = ('descr','create_date')
    pass

class SignalAdmin(admin.ModelAdmin):
    list_display = ('descr','type')
    pass

class IOSignalsDeviceTypeInline(admin.TabularInline):
    model = IOSignalsDeviceType
    extra = 0 
    pass

class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ('descr','create_date')
    inlines = [ IOSignalsDeviceTypeInline, ]
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
