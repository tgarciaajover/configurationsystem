from rest_framework import serializers
from setup.models import MachineHostSystem
from setup.models import PlantHostSystem
from setup.models import DeviceType
from setup.models import MonitoringDevice
from setup.models import MeasuredEntity
from setup.models import InputOutputPort
from setup.models import IdleReason
from setup.models import DisplayType
from setup.models import DisplayDevice
from setup.models import MeasuredEntityStateBehavior
from setup.models import MeasuredEntityTransitionState
from setup.models import IdleReasonHostSystem
from setup.models import MeasuredEntityScheduledEvent
from setup.models import Operator
from setup.models import MeasuredEntityOperator

import logging
import os
import logging.handlers
from utils.advutils import get_logger


logger = get_logger('iot_settings_serializers')


class SignalUnitSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    descr = serializers.CharField(max_length=60)
    create_date = serializers.DateTimeField('%Y-%m-%d %H:%M:%S.%f')

class SignalTypeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name =  serializers.CharField(max_length=60)
    class_name = serializers.CharField(max_length=200)
    protocol = serializers.CharField(max_length=1)
    create_date = serializers.DateTimeField('%Y-%m-%d %H:%M:%S.%f')

class SignalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    descr = serializers.CharField(max_length=200) 
    unit = SignalUnitSerializer(required=True)
    type = SignalTypeSerializer(required=True)
    create_date = serializers.DateTimeField('%Y-%m-%d %H:%M:%S.%f')

class IOSignalDeviceTypeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    i_o = serializers.CharField(max_length=1)
    signal = SignalSerializer(required=True)

class DeviceTypeSerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField('%Y-%m-%d %H:%M:%S.%f')
    io_signals = IOSignalDeviceTypeSerializer(many=True, read_only=True)

    class Meta:
        model = DeviceType
        fields = ( 'id', 'descr', 'create_date', 'io_signals' )

class InputOutputPortSerializer(serializers.ModelSerializer):
    signal_type = SignalSerializer(required=True)
    measured_entity = serializers.PrimaryKeyRelatedField(queryset=MeasuredEntity.objects.all())

    class Meta:
        model = InputOutputPort
        fields = ('id','port_label','signal_type','refresh_time_ms', 'measured_entity','transformation_text')

class MonitoringDeviceSerializer(serializers.ModelSerializer):
    device_type = DeviceTypeSerializer()
    create_date = serializers.DateTimeField('%Y-%m-%d %H:%M:%S.%f')
    io_ports = InputOutputPortSerializer(many=True,read_only=True)

    class Meta:
        model = MonitoringDevice
        fields= ('id', 'device_type','descr','serial','mac_address','ip_address','create_date','io_ports')

class MeasuredEntityBehaviorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=40)
    descr = serializers.CharField(max_length=160)
    behavior_text = serializers.CharField()
    create_date = serializers.DateTimeField('%Y-%m-%d %H:%M:%S.%f', required=False, read_only=True)

class MeasuredEntityStateBehaviorSerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField('%Y-%m-%d %H:%M:%S.%f', required=False, read_only=True)

    class Meta:
        model = MeasuredEntityStateBehavior
        fields = ('id', 'state_behavior_type', 'descr', 'behavior_text', 'create_date')

class MeasuredEntitySerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField('%Y-%m-%d %H:%M:%S.%f')
    behaviors = MeasuredEntityBehaviorSerializer(many=True,read_only=True)

    class Meta:
        model = MeasuredEntity
        fields= ('id', 'code', 'descr', 'type', 'create_date', 'behaviors')

class MeasuredEntityScheduledEventSerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField('%Y-%m-%d %H:%M:%S.%f', required=False, read_only=True)
    day_time = serializers.TimeField('%H:%M:%S.%f')

    class Meta:
        model = MeasuredEntityScheduledEvent
        fields = ('id', 'scheduled_event_type', 'descr', 'recurrences', 'create_date','day_time')

class IdleReasonSerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField('%Y-%m-%d %H:%M:%S.%f', required=False, read_only=True)
    
    class Meta:
        model = IdleReason
        fields = ('id', 'descr', 'group_cd', 'cause', 'classification','down', 'create_date')

class MeasuredEntityTransitionStateSerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField('%Y-%m-%d %H:%M:%S.%f', required=False, read_only=True)

    class Meta:
        model = MeasuredEntityTransitionState
        fields = ('id', 'state_from', 'reason_code', 'behavior', 'create_date')

class DisplayTypeSerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField('%Y-%m-%d %H:%M:%S.%f', required=False, read_only=True)

    class Meta:
        model = DisplayType
        fields = ('id', 'descr', 'pixels_width', 'pixels_height', 'text_color', 'back_color', 
                  'in_mode', 'out_mode', 'speed', 'line_spacing', 'letter_size', 
                  'vertical_alignment', 'horizontal_alignment', 'create_date' )

class DisplayDeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = DisplayType
        fields = ('id', 'descr', 'reference_cd', 'ip_address', 'port', 'display') 


class MachineHostSystemSerializer(serializers.Serializer):
    code = serializers.CharField(source='get_code', read_only=True)
    id_compania = serializers.CharField(max_length=60)
    id_sede = serializers.CharField(max_length=60)
    id_planta = serializers.CharField(max_length=60)
    id_grupo_maquina = serializers.CharField(max_length=60)
    id_maquina = serializers.CharField(max_length=60)
    descr = serializers.CharField(max_length=200)
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f", required=False, read_only=True)
    last_updttm = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f", required=False, read_only=True)
    tiempo_refresco = serializers.IntegerField()

    
    def create(self, validated_data):
        """
        Create and return a new `MachineHostSystem` instance, given the validated data.
        """
        machineHostSystem = MachineHostSystem()
        machineHostSystem.id_compania = validated_data.get('id_compania')
        machineHostSystem.id_sede = validated_data.get('id_sede')
        machineHostSystem.id_planta = validated_data.get('id_planta')
        machineHostSystem.id_grupo_maquina = validated_data.get('id_grupo_maquina')
        machineHostSystem.id_maquina = validated_data.get('id_maquina')
        machineHostSystem.descr = validated_data.get('descr')
        machineHostSystem.tiempo_refresco = validated_data.get('tiempo_refresco')
        if validated_data.get('create_date') != None:
            machineHostSystem.create_date = validated_data.get('create_date')

        if validated_data.get('last_updttm') != None:
            machineHostSystem.last_updttm = validated_data.get('last_updttm')

        machineHostSystem.code = str( validated_data.get('id_compania') +
                                         validated_data.get('id_sede')+
                                          validated_data.get('id_planta')+
                                           validated_data.get('id_grupo_maquina')+
                                            validated_data.get('id_maquina') )
        machineHostSystem.type = 'M'
        machineHostSystem.save()
        return machineHostSystem

    def update(self, instance, validated_data):
        """
        Update and return an existing `MachineHostSystem` instance, given the validated data.
        """
        instance = MachineHostSystem.objects.get(id_compania=validated_data.get('id_compania',instance.id_compania),
                                               id_sede=validated_data.get('id_sede',instance.id_sede),
                                               id_planta= validated_data.get('id_planta', instance.id_planta),
                                               id_grupo_maquina = validated_data.get('id_grupo_maquina',instance.id_grupo_maquina),
                                               id_maquina = validated_data.get('id_maquina',instance.id_maquina))
        instance.descr = validated_data.get('descr')
        if validated_data.get('create_date') != None:
            instance.create_date = validated_data.get('create_date')
        if validated_data.get('last_updttm') != None:
            instance.last_updttm = validated_data.get('last_updttm')
        instance.save()
        return instance    

class PlantHostSystemSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    id_compania = serializers.CharField(max_length=60)
    id_sede = serializers.CharField(max_length=60)
    id_planta = serializers.CharField(max_length=60)
    descr = serializers.CharField(max_length=200)
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f", required=False, read_only=True)
    last_updttm = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f", required=False, read_only=True)

    def create(self, validated_data):
        """
        Create and return a new `PlantHostSystem` instance, given the validated data.
        """
        plantHostSystem = PlantHostSystem()
        plantHostSystem.id_compania = validated_data.get('id_compania')
        plantHostSystem.id_sede = validated_data.get('id_sede')
        plantHostSystem.id_planta = validated_data.get('id_planta')
        plantHostSystem.descr = validated_data.get('descr')

        if validated_data.get('create_date') != None:
            plantHostSystem.create_date = validated_data.get('create_date')

        if validated_data.get('last_updttm') != None:
            plantHostSystem.last_updttm = validated_data.get('last_updttm')

        plantHostSystem.code = str( validated_data.get('id_compania') +
                                       validated_data.get('id_sede') +
                                        validated_data.get('id_planta') )
        plantHostSystem.type = 'P'
        plantHostSystem.save()
        return plantHostSystem

    def update(self, instance, validated_data):
        """
        Update and return an existing `Company` instance, given the validated data.
        """
        instance = PlantHostSystem.objects.get(id_compania=validated_data.get('id_compania',instance.id_compania),
                                               id_sede=validated_data.get('id_sede',instance.id_sede),
                                               id_planta= validated_data.get('id_planta', instance.id_planta))
        instance.descr =  validated_data.get('descr')

        if validated_data.get('last_updttm') != None:
            instance.last_updttm = validated_data.get('last_updttm')

        if validated_data.get('create_date') != None:
            instance.create_date = validated_data.get('create_date')
            
        instance.save()
        return instance


class IdleReasonHostSystemSerializer(serializers.Serializer):
    id_compania = serializers.CharField(max_length=60)
    id_sede = serializers.CharField(max_length=60)
    id_planta = serializers.CharField(max_length=60)
    id_razon_parada = serializers.CharField(max_length=60)
    descr = serializers.CharField(max_length=200)
    grupo_razon_parada = serializers.CharField(max_length=60)
    causa_raiz_parada = serializers.CharField(max_length=60)
    clasificacion = serializers.CharField(max_length=1)
    afecta_capacidad = serializers.CharField(max_length=1)
    

    def create(self, validated_data):
        """
        Create and return a new `IdleReasonHostSystem` instance, given the validated data.
        """
        logger.info('In IdleReasonHostSystem serializer method create')
        idleReasonHostSystem = IdleReasonHostSystem()
        idleReasonHostSystem.id_compania = validated_data.get('id_compania')
        idleReasonHostSystem.id_sede = validated_data.get('id_sede')
        idleReasonHostSystem.id_planta = validated_data.get('id_planta')
        idleReasonHostSystem.id_razon_parada = validated_data.get('id_razon_parada')
        idleReasonHostSystem.descr = validated_data.get('descr')
        idleReasonHostSystem.group_cd = validated_data.get('grupo_razon_parada')
        idleReasonHostSystem.cause = validated_data.get('causa_raiz_parada')
        idleReasonHostSystem.down = validated_data.get('afecta_capacidad')
        idleReasonHostSystem.classification = validated_data.get('clasificacion')

        idleReasonHostSystem.save()
        return idleReasonHostSystem

    def update(self, instance, validated_data):
        """
        Update and return an existing `Idle Reason` instance, given the validated data.
        """
        logger.info('In IdleReasonHostSystem serializer method update')
        instance = IdleReasonHostSystem.objects.get(id_compania=validated_data.get('id_compania',instance.id_compania),
                                               id_sede=validated_data.get('id_sede',instance.id_sede),
                                               id_planta= validated_data.get('id_planta', instance.id_planta),
					       id_razon_parada = validated_data.get('id_razon_parada', instance.id_razon_parada))
        instance.descr =  validated_data.get('descr')
        instance.group_cd = validated_data.get('grupo_razon_parada')
        instance.cause = validated_data.get('causa_raiz_parada')
        instance.down = validated_data.get('afecta_capacidad')        
        instance.classification = validated_data.get('clasificacion')
        if validated_data.get('last_updttm') != None:
            instance.last_updttm = validated_data.get('last_updttm')
        instance.save()
        return instance


class IdleReasonHostSystemOuputSerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField('%Y-%m-%d %H:%M:%S.%f',  required=False, read_only=True)

    class Meta:
        model = IdleReasonHostSystem
        fields = ('id', 'descr', 'group_cd', 'cause', 'classification', 'down', 'create_date')


class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = '__all__'


class MeasuredEntityOperatorSerializer(serializers.Serializer):
    class Meta:
        model = MeasuredEntityOperator
        fields = ('operator', 'measured_entity')