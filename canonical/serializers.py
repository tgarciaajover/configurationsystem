from rest_framework import serializers
from canonical.models import Compania
from canonical.models import Sede
from canonical.models import Planta
from canonical.models import RazonParada
from canonical.models import GrupoMaquina
from canonical.models import Maquina
from canonical.models import PlanProduccion
from canonical.models import OrdenProduccionPlaneada
from canonical.models import ParadaPlaneada
from canonical.models import ActivityRegister

from django.contrib.auth.models import User


class CompaniaSerializer(serializers.Serializer):
    id_compania = serializers.CharField(max_length=60)
    descr = serializers.CharField(max_length=200)
    
    def create(self, validated_data):
        """
        Create and return a new `Company` instance, given the validated data.
        """
        return Compania.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Company` instance, given the validated data.
        """
        instance = Compania.objects.get(id_compania=validated_data.get('id_compania',instance.id_compania))
        instance.id_compania = validated_data.get('id_compania',instance.id_compania)
        instance.descr = validated_data.get('descr',instance.descr)
        instance.save()
        return instance

class SedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sede
        fields = ('id_compania', 'id_sede', 'descr', 'create_date', 'last_updttm')

class PlantaSerializer(serializers.Serializer):
    id_compania = serializers.CharField(max_length=60)
    id_sede = serializers.CharField(max_length=60)
    id_planta = serializers.CharField(max_length=60)
    descr = serializers.CharField(max_length=200)
    last_updttm = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    def create(self, validated_data):
        """
        Create and return a new `Planta` instance, given the validated data.
        """
        planta = Planta.objects.create(**validated_data)
        return planta

    def update(self, instance, validated_data):
        """
        Update and return an existing `Planta` instance, given the validated data.
        """
        instance = Planta.objects.get(id_compania=validated_data.get('id_compania',instance.id_compania),
                                      id_sede=validated_data.get('id_sede',instance.id_sede),
                                      id_planta= validated_data.get('id_planta', instance.id_planta))
        instance.descr =  validated_data.get('descr')
        instance.last_updttm = validated_data.get('last_updttm')
        instance.save()
        return instance

class RazonParadaSerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f", input_formats=["%Y-%m-%d %H:%M:%S.%f"], required=False, read_only=True)
    last_updttm = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f", input_formats=["%Y-%m-%d %H:%M:%S.%f"], required=False, read_only=True)

    class Meta:
        model = RazonParada
        fields = ( 'id_compania', 'id_sede','id_planta', 
                   'id_razon_parada', 'descr', 'grupo_razon_parada',
                   'causa_raiz_parada', 'afecta_capacidad', 'clasificacion',
                   'create_date', 'last_updttm' )

class GrupoMaquinaSerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f", input_formats=["%Y-%m-%d %H:%M:%S.%f"], required=False, read_only=True)
    last_updttm = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f", input_formats=["%Y-%m-%d %H:%M:%S.%f"], required=False, read_only=True)

    class Meta: 
        model = GrupoMaquina
        fields = ( 'id_compania', 'id_sede','id_planta', 
                   'id_grupo_maquina', 'descr', 
                   'create_date', 'last_updttm' )

class MaquinaSerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f", input_formats=["%Y-%m-%d %H:%M:%S.%f"], required=False, read_only=True)
    last_updttm = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f", input_formats=["%Y-%m-%d %H:%M:%S.%f"], required=False, read_only=True)

    class Meta:
        model = Maquina
        fields = ( 'id_compania', 'id_sede','id_planta', 
                   'id_grupo_maquina', 'id_maquina',
                   'descr', 'estado_actual', 'tasa_vel_esperada',
                   'tiempo_esperado_config', 'factor_conversion_kg_ciclo',
                   'factor_conversion_mil_ciclo', 'factor_conversion_emp_ciclo',
                   'descripcion_sin_trabajo', 'create_date', 'last_updttm' )

class PlanProduccionSerializer(serializers.ModelSerializer):
    last_updttm = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f", input_formats=["%Y-%m-%d %H:%M:%S.%f"], required=False, read_only=True)

    class Meta:
        model = PlanProduccion
        fields = ( 'id_compania', 'id_sede','id_planta',
                   'id_grupo_maquina', 'id_maquina', 'ano',
                   'mes',  'create_date', 'last_updttm' )

class OrdenProduccionPlaneadaSerializer(serializers.ModelSerializer):
    fechahora_inicial = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f", input_formats=["%Y-%m-%d %H:%M:%S"])
    fechahora_final = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f", input_formats=["%Y-%m-%d %H:%M:%S"])
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f", input_formats=["%Y-%m-%d %H:%M:%S.%f"], required=False, read_only=True)
    last_updttm = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f", input_formats=["%Y-%m-%d %H:%M:%S.%f"], required=False, read_only=True)

    class Meta:
        model = OrdenProduccionPlaneada
        fields = ( 'id_compania', 'id_sede','id_planta',
                   'id_grupo_maquina', 'id_maquina', 'ano',
                   'mes', 'id_produccion', 'id_articulo',
                   'descr_articulo', 'fechahora_inicial',
                   'fechahora_final', 'num_horas', 'cantidad_producir',
                   'tasa_esperada', 'velocidad_esperada', 'tasa_vel_esperada', 
                   'factor_conversion_kg_ciclo', 'factor_conversion_mil_ciclo',
                   'factor_conversion_emp_ciclo', 'create_date', 'last_updttm' )

class ParadaPlaneadaSerializer(serializers.ModelSerializer):
    fechahora_inicial = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f", input_formats=["%Y-%m-%d %H:%M:%S"])
    fechahora_final = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f", input_formats=["%Y-%m-%d %H:%M:%S"])
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f", input_formats=["%Y-%m-%d %H:%M:%S.%f"], required=False, read_only=True)
    last_updttm = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f", input_formats=["%Y-%m-%d %H:%M:%S.%f"], required=False, read_only=True)
    
    class Meta:
        model = ParadaPlaneada
        fields = ( 'id_compania', 'id_sede','id_planta',
                   'id_grupo_maquina', 'id_maquina', 'ano',
                   'mes', 'fechahora_inicial', 'fechahora_final',
                   'create_date', 'last_updttm' )

class ActivityRegisterSerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f", input_formats=["%Y-%m-%d %H:%M:%S.%f"], required=False, read_only=True)
    last_updttm = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f", input_formats=["%Y-%m-%d %H:%M:%S.%f"], required=False, read_only=True)

    class Meta:
        model = ActivityRegister
        fields = ( 'id_compania', 'id_sede','id_planta',
                   'id_grupo_maquina', 'id_maquina', 'ano',
                   'mes', 'tipo_actividad', 'id_razon_parada',
                   'id_produccion', 'create_date', 'last_updttm' )

class UserSeralizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password' : {'write_only':True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# class DashboardSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Dashboard
#         fields = '__all__'
#
# class ChartSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Chart
#         fields = '__all__'