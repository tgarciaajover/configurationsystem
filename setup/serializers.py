from rest_framework import serializers
from setup.models import MachineHostSystem
from setup.models import PlantHostSystem
from setup.models import DeviceType
from setup.models import MonitoringDevice


class SignalUnitSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    descr = serializers.CharField(max_length=60)
    create_date = serializers.DateTimeField('%Y-%b-%d %H:%M:%S.%f')

class SignalTypeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name =  serializers.CharField(max_length=60)
    class_name = serializers.CharField(max_length=200) 
    create_date = serializers.DateTimeField('%Y-%b-%d %H:%M:%S.%f')

class SignalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    descr = serializers.CharField(max_length=200) 
    unit = SignalUnitSerializer(required=True)
    type = SignalTypeSerializer(required=True)
    create_date = serializers.DateTimeField('%Y-%b-%d %H:%M:%S.%f')

class IOSignalDeviceTypeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    i_o = serializers.CharField(max_length=1)
    signal = SignalSerializer(required=True)

class DeviceTypeSerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField('%Y-%b-%d %H:%M:%S.%f')
    io_signals = IOSignalDeviceTypeSerializer(many=True, read_only=True)

    class Meta:
        model = DeviceType
        fields = ( 'id', 'descr', 'create_date', 'io_signals' )

class InputOutputPortSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    port_label = serializers.CharField(max_length=10)
    signal_type = SignalSerializer(required=True)
    meaured_entity = serializers.IntegerField(read_only=True)
    transformation_text = serializer.CharField()

class MonitoringDevicesSerializer(serializers.ModelSerializer):
    type = DeviceTypeSerializer()
    create_date = serializers.DateTimeField('%Y-%b-%d %H:%M:%S.%f')
    io_ports = InputOutputPortSerializer(many=True,read_only=True)

    class Meta:
        model = MeonitoringDevice
        fields= ('type','descr','serial','mac_address','ip_address','create_date','io_ports')


class MachineHostSystemSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=20)
    id_compania = serializers.CharField(max_length=60)
    id_sede = serializers.CharField(max_length=60)
    id_planta = serializers.CharField(max_length=60)
    id_grupo_maquina = serializers.CharField(max_length=60)
    id_maquina = serializers.CharField(max_length=60)
    descr = serializers.CharField(max_length=200)
    last_updttm = serializers.DateTimeField()
    
    def create(self, validated_data):
        """
        Create and return a new `MachineHostSystem` instance, given the validated data.
        """
        print ('here i am create')
        machineHostSystem = MachineHostSystem()
        machineHostSystem.id_compania = validated_data.get('id_compania')
        machineHostSystem.id_sede = validated_data.get('id_sede')
        machineHostSystem.id_planta = validated_data.get('id_planta')
        machineHostSystem.id_grupo_maquina = validated_data.get('id_grupo_maquina')
        machineHostSystem.id_maquina = validated_data.get('id_maquina')
        machineHostSystem.descr = validated_data.get('descr')
        machineHostSystem.last_updttm = validated_data.get('last_updttm')
        machineHostSymtem.code = str( hash ( validated_data.get('id_compania') +
                                         validated_data.get('id_sede')+
                                          validated_data.get('id_planta')+
                                           validated_data.get('id_grupo_maquina')+
                                            validated_data.get('id_maquina') ) )
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
        instance.descr =  validated_data.get('descr')
        instance.last_updttm = validated_data.get('last_updttm')
        instance.save()
        print ('here i am update')
        return instance    

class PlantHostSystemSerializer(serializers.Serializer):
    id_compania = serializers.CharField(max_length=60)
    id_sede = serializers.CharField(max_length=60)
    id_planta = serializers.CharField(max_length=60)
    descr = serializers.CharField(max_length=200)
    last_updttm = serializers.DateTimeField()

    def create(self, validated_data):
        """
        Create and return a new `PlantHostSystem` instance, given the validated data.
        """
        print ('here i am create')
        plantHostSystem = PlantHostSystem()
        plantHostSystem.id_compania = validated_data.get('id_compania')
        plantHostSystem.id_sede = validated_data.get('id_sede')
        plantHostSystem.id_planta = validated_data.get('id_planta')
        plantHostSystem.descr = validated_data.get('descr')
        plantHostSystem.last_updttm = validated_data.get('last_updttm')
        plantHostSystem.code = str( hash ( validated_data.get('id_compania') +
                                       validated_data.get('id_sede') +
                                        validated_data.get('id_planta') ) )
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
        instance.last_updttm = validated_data.get('last_updttm')
        instance.save()
        print ('here i am update')
        return instance

