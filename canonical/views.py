from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import parser_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser

from canonical.models import Compania
from canonical.models import Sede
from canonical.models import Planta
from canonical.models import RazonParada
from canonical.models import GrupoMaquina
from canonical.models import Maquina
from canonical.models import PlanProduccion
from canonical.models import OrdenProduccionPlaneada
from canonical.models import ParadaPlaneada
from canonical.serializers import CompaniaSerializer
from canonical.serializers import SedeSerializer
from canonical.serializers import PlantaSerializer
from canonical.serializers import RazonParadaSerializer
from canonical.serializers import GrupoMaquinaSerializer
from canonical.serializers import MaquinaSerializer
from canonical.serializers import PlanProduccionSerializer
from canonical.serializers import OrdenProduccionPlaneadaSerializer
from canonical.serializers import ParadaPlaneadaSerializer
from setup.serializers import PlantHostSystemSerializer

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def compania_list(request, format=None):
    """
    Lista todas las companias, or crea una nueva compania.
    """

    if request.method == 'GET':
        companias = Compania.objects.all()
        serializer = CompaniaSerializer(companias, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CompaniaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated, ))
def compania_detail(request, pk, format=None):
    """
    Obtiene, actualiza or borra una compania.
    """

    try:
        compania = Compania.objects.get(pk=pk)
    except Compania.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CompaniaSerializer(compania)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CompaniaSerializer(compania, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        compania.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def sede_list(request, format=None):
    """
    Lista todas las sedes, or crea una nueva sede.
    """

    if request.method == 'GET':
        sedes = Sede.objects.all()
        serializer = SedeSerializer(sedes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SedeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated, ))
def sede_detail(request, pk, format=None):
    """
    Obtiene, actualiza or borra una sede.
    """
   
    try:
        sede = Sede.objects.get(pk=pk)
    except Sede.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SedeSerializer(sede)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SedeSerializer(sede, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        sede.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes((AllowAny, ))
@parser_classes((JSONParser,))
def planta_list(request, format=None):
    """
    Lista todas las plantas, or crea una nueva planta.
    """

    if request.method == 'GET':
        plantas = Planta.objects.all()
        serializer = PlantaSerializer(plantas, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            planta = Planta.objects.get(id_compania = data['id_compania'], 
                                        id_sede = data['id_sede'], 
	                                id_planta = data['id_planta'])
            return Response(status=status.HTTP_302_FOUND)
        except Planta.DoesNotExist:
            serializer_p = PlantaSerializer(data=data)
            serializer_phs = PlantHostSystemSerializer(data=data)
            if serializer_p.is_valid() and serializer_phs.is_valid():
                serializer_p.save()
                serializer_phs.save()
                return JsonResponse(serializer_p.data, status=201)
            return JsonResponse(serializer_p.errors, status=400) 

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated, ))
def planta_detail(request, pk, format=None):
    """
    Obtiene, actualiza or borra una planta.
    """

    try:
        data = JSONParser(request.data)
        planta = Planta.objects.get(id_compania=data.get('id_compania'), 
                                     id_sede = data.get('id_sede'), 
                                      id_planta = data.get('id_planta'))
        planths = PlantHostSystem.objects.get(id_compania=data.get('id_compania'), 
                                               id_sede = data.get('id_sede'), 
                                                id_planta = data.get('id_planta'))
    except Planta.DoesNotExist:
    #except PlantHostSystem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PlantaSerializer(planta)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PlantaSerializer(planta, data=request.data)
        serializer_phs = PlantHostSystemSerializer(planths, data.request.data)
        if serializer.is_valid() and serializer_phs.is_valid():
            serializer.save()
            serializer_phs.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        planta.delete()
        planths.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def razon_parada_list(request, format=None):
    """
    Lista todas las razones de parada, or crea una nueva razon de parada.
    """

    if request.method == 'GET':
        razonesparada = RazonParada.objects.all()
        serializer = RazonParadaSerializer(razonesparada, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RazonParadaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated, ))
def razon_parada_detail(request, pk, format=None):
    """
    Obtiene, actualiza or borra una razon de parada.
    """

    try:
        razonparada = RazonParada.objects.get(pk=pk)
    except RazonParada.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RazonParadaSerializer(razonparada)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RazonParadaSerializer(razonparada, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        razonparada.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def grupo_maquina_list(request, format=None):
    """
    Lista todas los grupos de maquina, or crea un nuevo grupo de maquina.
    """
   
    if request.method == 'GET':
        grupomaquina = GrupoMaquina.objects.all()
        serializer = GrupoMaquinaSerializer(grupomaquina, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = GrupoMaquinaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated, ))
def grupo_maquina_detail(request, pk, format=None):
    """
    Obtiene, actualiza or borra un grupo de maquina.
    """

    try:
        grupomaquina = GrupoMaquina.objects.get(pk=pk)
    except GrupoMaquina.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GrupoMaquinaSerializer(grupomaquina)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        serializer = GrupoMaquinaSerializer(grupomaquina, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        grupomaquina.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def maquina_list(request, format=None):
    """
    Lista todas las maquinas, or crea una nueva maquina.
    """

    if request.method == 'GET':
        maquina = Maquina.objects.all()
        serializer = MaquinaSerializer(maquina, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            maquina = Maquina.objects.get(id_compania = data.get('id_compania'),
                                           id_sede = data.get('id_sede'),
                                            id_planta = data.get('id_planta'),
                                             id_grupo_maquina = data.get('id_grupo_maquina'),
                                              id_maquina = data.get('id_maquina'))
            return JsonResponse(data, status=301) # HTTP_FOUND
        except Maquina.DoesNotExist:
            serializer_p = MaquinaSerializer(data=data)
            serializer_mhs = MachineHostSystemSerializer(data=data)
            if serializer_p.is_valid() and serializer_mhs.is_valid():
                serializer_.save()
                serializer_mhs.save()
                return serializer_mhs(serializer_p.data, status=201)
            return Response(serializer_p.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated, ))
def maquina_detail(request, pk, format=None):
    """
    Obtiene, actualiza or borra una maquina.
    """

    try:
        maquina = Maquina.objects.get(id_compania = data.get('id_compania'),
                                           id_sede = data.get('id_sede'),
                                            id_planta = data.get('id_planta'),
                                             id_grupo_maquina = data.get('id_grupo_maquina'),
                                              id_maquina = data.get('id_maquina'))
        machinehs = MachineHostSystem.objects.get( id_compania = data.get('id_compania'),
                                            id_sede = data.get('id_sede'),
                                            id_planta = data.get('id_planta'),
                                             id_grupo_maquina = data.get('id_grupo_maquina'),
                                              id_maquina = data.get('id_maquina'))

    except Maquina.DoesNotExist:
    #except MachineHostSystem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MaquinaSerializer(maquina)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MaquinaSerializer(maquina, data=request.data)
        serializer_mhs = MachineHostSystemSerializer( machinehs, data=request.data)
        if serializer.is_valid() and serializer_mhs.is_valid():
            serializer.save()
            serializer_mhs.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        maquina.delete()
        machinehs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def plan_produccion_list(request, format=None):
    """
    Lista todos los planes de produccion, or crea un nuevo plan de produccion.
    """

    if request.method == 'GET':
        planproduccion = PlanProduccion.objects.all()
        serializer = PlanProduccionSerializer(planproduccion, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PlanProduccionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated, ))
def plan_produccion_detail(request, pk, format=None):
    """
    Obtiene, actualiza or borra un plan de produccion.
    """

    try:
        planproduccion = PlanProduccion.objects.get(pk=pk)
    except PlanProduccion.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PlanProduccionSerializer(planproduccion)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PlanProduccionSerializer(planproduccion, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        planproduccion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def orden_produccion_planeada_list(request, format=None):
    """
    Lista todos las ordenes de produccion planeada, or crea una nueva orden de produccion planeada.
    """

    if request.method == 'GET':
        ordenproduccionplaneada = OrdenProduccionPlaneada.objects.all()
        serializer = OrdenProduccionPlaneadaSerializer(ordenproduccionplaneada, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = OrdenProduccionPlaneadaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated, ))
def orden_produccion_planeada_detail(request, pk, format=None):
    """
    Obtiene, actualiza or borra una order de produccion planeada.
    """

    try:
        ordenproduccionplaneada = OrdenProduccionPlaneada.objects.get(pk=pk)
    except OrdenProduccionPlaneada.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrdenProduccionPlaneadaSerializer(ordenproduccionplaneada)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = OrdenProduccionPlaneadaSerializer(ordenproduccionplaneada, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        ordenproduccionplaneada.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def parada_planeada_list(request, format=None):
    """
    Lista todos las paradas planeadas, or crea una nueva parada planeada.
    """

    if request.method == 'GET':
        paradaplaneada = ParadaPlaneada.objects.all()
        serializer = ParadaPlaneadaSerializer(paradaplaneada, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ParadaPlaneadaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated, ))
def parada_planeada_detail(request, pk, format=None):
    """
    Obtiene, actualiza or borra una parada planeada.
    """

    try:
        paradaplaneada = ParadaPlaneada.objects.get(pk=pk)
    except ParadaPlaneada.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ParadaPlaneadaSerializer(paradaplaneada)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ParadaPlaneadaSerializer(paradaplaneada, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        paradaplaneada.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
