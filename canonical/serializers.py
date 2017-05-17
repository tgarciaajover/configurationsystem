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
        instance.last_updttm =  validated_data.get('descr',instance.last_updttm)
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
    last_updttm = serializers.DateTimeField()

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
    class Meta:
        model = RazonParada
        fields = ( 'id_compania', 'id_sede','id_planta', 
                   'id_razon_parada', 'descr', 'grupo_razon_parada',
                   'causa_raiz_parada', 'afecta_capacidad',
                   'create_date', 'last_updttm' )

class GrupoMaquinaSerializer(serializers.ModelSerializer):
    class Meta: 
        model = GrupoMaquina
        fields = ( 'id_compania', 'id_sede','id_planta', 
                   'id_grupo_maquina', 'descr', 
                   'create_date', 'last_updttm' )

class MaquinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maquina
        fields = ( 'id_compania', 'id_sede','id_planta', 
                   'id_grupo_maquina', 'id_maquina',
                   'descr', 'estado_actual',
                   'create_date', 'last_updttm' )

class PlanProduccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanProduccion
        fields = ( 'id_compania', 'id_sede','id_planta',
                   'id_grupo_maquina', 'id_maquina', 'ano',
                   'mes',  'create_date', 'last_updttm' )

class OrdenProduccionPlaneadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenProduccionPlaneada
        fields = ( 'id_compania', 'id_sede','id_planta',
                   'id_grupo_maquina', 'id_maquina', 'ano',
                   'mes', 'id_produccion', 'id_articulo',
                   'descr_articulo', 'fechahora_inicial',
                   'fechahora_final', 'num_horas', 'cantidad_producir',
                   'tasa_esperada', 'velocidad_esperada', 
                   'create_date', 'last_updttm' )

class ParadaPlaneadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParadaPlaneada
        fields = ( 'id_compania', 'id_sede','id_planta',
                   'id_grupo_maquina', 'id_maquina', 'ano',
                   'mes', 'fechahora_inicial', 'fechahora_final',
                   'create_date', 'last_updttm' )


