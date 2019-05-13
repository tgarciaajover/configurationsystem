from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import parser_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

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

from canonical.models import ActivityRegister

from setup.models import PlantHostSystem
from setup.models import MachineHostSystem
from setup.models import IdleReasonHostSystem
from setup.models import Employee

from setup.serializers import PlantHostSystemSerializer
from setup.serializers import MachineHostSystemSerializer
from setup.serializers import IdleReasonHostSystemSerializer
from setup.serializers import IdleReasonHostSystemOuputSerializer

from canonical.tasks import delReasonCode
from canonical.tasks import putReasonCode
from canonical.tasks import putActivityRegister

from django.views.generic import ListView
from django.views.generic import CreateView
from django import forms
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.urls import reverse
from django.http import HttpResponseRedirect

import setup.defaults as defaults
import requests

import datetime

import logging
import os
import logging.handlers

from django.core import serializers

from rest_framework import viewsets
from django.contrib.auth.models import User
from canonical.serializers import UserSeralizer

from rest_framework.views import APIView

# Get an instance of a logger
LOG_FILENAME = 'iotsettings.log'

# Check if log exists and should therefore be rolled
needRoll = os.path.isfile(LOG_FILENAME)

logger = logging.getLogger('canonical.views')

fh = logging.handlers.RotatingFileHandler(LOG_FILENAME, backupCount=5)
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

@api_view(['POST', ])
@permission_classes((IsAuthenticated, ))
@parser_classes((JSONParser,))
def maquinas_variables(request, format=None):
    if request.method == 'POST':
        request_data = request.data

        json_data = []

        for compania in request_data['companias']:
            for sede in compania['sedes']:
                for planta in sede['plantas']:
                    for grup in planta['grupos_maquinas']:
                        for maquina in grup['maquinas']:
                            json_append = {
                                'company': compania['id_compania'],
                                'location': sede['id_sede'],
                                'plant': planta['id_planta'],
                                'machineGroup': grup['id_grupo_maquina'],
                                'machineId': maquina['id_maquina'],
                                'startDttm': request_data['startDttm'],
                                'endDttm': request_data['endDttm'],
                                'variable': request_data['variable']
                            }

                            json_data.append(json_append)

        for data in json_data:
            # TODO: Cambiar URL
            req = requests.get(url='http://192.168.1.171:8111/iotserver/Trend', params=data)
            data['value'] = req.json()

        return Response(json_data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST', ])
@permission_classes((IsAuthenticated, ))
@parser_classes((JSONParser,))
def variables_comunes(request, format=None):
    if request.method == 'POST':
        request_data = request.data

        json_data = []

        for compania in request_data['companias']:
            for sede in compania['sedes']:
                for planta in sede['plantas']:
                    for grup in planta['grupos_maquinas']:
                        for maquina in grup['maquinas']:
                            json_append = {
                                'company': compania['id_compania'],
                                'location': sede['id_sede'],
                                'plant': planta['id_planta'],
                                'machineGroup': grup['id_grupo_maquina'],
                                'machineId': maquina['id_maquina']
                            }

                            json_data.append(json_append)

        variables = []
        initial = True

        for data in json_data:
            # TODO: Cambiar URL
            req = requests.get(url='http://192.168.1.171:8111/iotserver/Status', params=data)
            print(json.dumps(json.loads(req.text), indent=4))
            json_info = json.loads(req.text)

            if initial == True:
                for info in json_info:
                    variables.append(info['key'])
                    initial = False
            elif len(variables) > 0:
                temp = []
                for info in json_info:
                    temp.append(info['key'])

                variables = list(set(variables).intersection(temp))
            else:
                break

        return_json = {
            'kpis': variables
        }

        return Response(return_json, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def arbol(request, format=None):
    if request.method == 'GET':
        json_data = {
            'companias': []
        }

        companias = Compania.objects.all()

        for comp in companias:
            push_compania = {
                'id_compania': comp.id_compania,
                'descr': comp.descr,
                'sedes': []
            }

            json_data['companias'].append(push_compania)

            index_compania = len(json_data['companias']) - 1

            sedes = Sede.objects.filter(id_compania=comp.id_compania)

            for sede in sedes:
                push_sede = {
                    'id_sede': sede.id_sede,
                    'id_compania': sede.id_compania,
                    'descr': sede.descr,
                    'plantas': []
                }

                json_data['companias'][index_compania]['sedes'].append(push_sede)

                index_sede = len(json_data['companias'][index_compania]['sedes']) - 1

                plantas = Planta.objects.filter(id_sede=sede.id_sede, id_compania=comp.id_compania)

                for planta in plantas:
                    push_planta = {
                        'id_planta': planta.id_planta,
                        'id_sede': planta.id_sede,
                        'id_compania': planta.id_compania,
                        'descr': planta.descr,
                        'grupos_maquinas': []
                    }

                    json_data['companias'][index_compania]['sedes'][index_sede]['plantas'].append(push_planta)

                    index_planta = len(json_data['companias'][index_compania]['sedes'][index_sede]['plantas']) - 1

                    grupos_maquinas = GrupoMaquina.objects.filter(id_planta=planta.id_planta, id_sede=sede.id_sede, id_compania=comp.id_compania)

                    for grup in grupos_maquinas:
                        push_grup = {
                            'id_grupo_maquina': grup.id_grupo_maquina,
                            'id_planta': grup.id_planta,
                            'id_sede': grup.id_sede,
                            'id_compania': grup.id_compania,
                            'descr': grup.descr,
                            'maquinas': []
                        }

                        json_data['companias'][index_compania]['sedes'][index_sede]['plantas'][index_planta]['grupos_maquinas'].append(push_grup)

                        index_grup = len(json_data['companias'][index_compania]['sedes'][index_sede]['plantas'][index_planta]['grupos_maquinas']) - 1

                        maquinas = Maquina.objects.filter(id_grupo_maquina=grup.id_grupo_maquina, id_planta=planta.id_planta, id_sede=sede.id_sede, id_compania=comp.id_compania)

                        for maquina in maquinas:
                            push_maquina = {
                                'id_maquina': maquina.id_maquina,
                                'id_grupo_maquina': maquina.id_grupo_maquina,
                                'id_planta': maquina.id_planta,
                                'id_sede': maquina.id_sede,
                                'id_compania': maquina.id_compania,
                                'descr': maquina.descr,
                            }

                            json_data['companias'][index_compania]['sedes'][index_sede]['plantas'][index_planta]['grupos_maquinas'][index_grup]['maquinas'].append(push_maquina)

        return Response(json_data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
@parser_classes((JSONParser,))
def compania_list(request, format=None):
    """
    Lista todas las companias, or crea una nueva compania.
    """
    if request.method == 'GET':
        companias = Compania.objects.all()
        serializer = CompaniaSerializer(companias, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            compania = Compania.objects.get(id_compania = data['id_compania'])
            return Response(status=status.HTTP_302_FOUND)
        except Compania.DoesNotExist:
            serializer = CompaniaSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.error(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated, ))
@parser_classes((JSONParser,))
def compania_detail(request, pk, format=None):
    """
    Obtiene, actualiza or borra una compania.
    """
    try:
        data = JSONParser().parse(request)
        companias = Compania.objects.filter(id_compania=data.get('id_compania'))
    except Compania.DoesNotExist:
        if request.method == 'DELETE':
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if len(companias) > 1:
            return Response(serializer.errors, status=status.HTTP_412_PRECONDITION_FAILED)
        
        compania = companias[0]
        serializer = CompaniaSerializer(compania)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if len(companias) > 1:
            return Response(serializer.errors, status=status.HTTP_412_PRECONDITION_FAILED)

        compania = companias[0]
        serializer = CompaniaSerializer(compania, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            logger.error(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        for compania in companias:
            compania.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
@parser_classes((JSONParser,))
def sede_list(request, format=None):
    """
    Lista todas las sedes, or crea una nueva sede.
    """

    if request.method == 'GET':
        sedes = Sede.objects.all()
        serializer = SedeSerializer(sedes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            sede = Sede.objects.get(id_compania=data.get('id_compania'), 
                                 id_sede = data.get('id_sede'))
            return Response(status=status.HTTP_302_FOUND)
        except Sede.DoesNotExist:
            serializer = SedeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.error(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated, ))
@parser_classes((JSONParser,))
def sede_detail(request, pk, format=None):
    """
    Obtiene, actualiza or borra una sede.
    """
   
    try:
        data = JSONParser().parse(request)
        sede = Sede.objects.get(id_compania=data.get('id_compania'), 
                                 id_sede = data.get('id_sede'))
    except Sede.DoesNotExist:
        if request.method == 'DELETE':
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SedeSerializer(sede)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SedeSerializer(sede, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            logger.error(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        sede.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
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
            planta = Planta.objects.get(id_compania = data.get('id_compania') , 
                                        id_sede = data.get('id_sede'), 
	                                id_planta = data.get('id_planta'))
            return Response(status=status.HTTP_302_FOUND)
        except Planta.DoesNotExist:
            serializer_p = PlantaSerializer(data=data)
            serializer_phs = PlantHostSystemSerializer(data=data)
            print(serializer_p)
            print(serializer_phs)
            if (serializer_p.is_valid() and serializer_phs.is_valid()):
                serializer_p.save()
                serializer_phs.save()
                return JsonResponse(serializer_p.data, status=201)
            else:
                logger.error(serializer_p.errors)
                logger.error(serializer_phs.errors)
                print('ERRORS')
                print(serializer_p.errors)
                print(serializer_phs.errors)
                return JsonResponse(serializer_p.errors, status=400) 

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated, ))
@parser_classes((JSONParser,))
def planta_detail(request, pk, format=None):
    """
    Obtiene, actualiza or borra una planta.
    """
    
    try:
        data = JSONParser().parse(request)
        planta = Planta.objects.get(id_compania=data.get('id_compania'), 
                                     id_sede = data.get('id_sede'), 
                                      id_planta = data.get('id_planta'))
        planths = PlantHostSystem.objects.get(id_compania=data.get('id_compania'), 
                                               id_sede = data.get('id_sede'), 
                                                id_planta = data.get('id_planta'))
    except ( Planta.DoesNotExist, PlantHostSystem.DoesNotExist ) as e:
        if request.method == 'DELETE':
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            logger.error('The plant already exists')
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PlantaSerializer(planta)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PlantaSerializer(planta, data=data)
        serializer_phs = PlantHostSystemSerializer(planths, data=data)
        if serializer.is_valid() and serializer_phs.is_valid():
            serializer.save()
            serializer_phs.save()
            return Response(serializer.data)
        else:
            logger.error(serializer.errors)
            logger.error(serializer_phs.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        planta.delete()
        planths.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
@parser_classes((JSONParser,))
def razon_parada_list(request, format=None):
    """
    Lista todas las razones de parada, or crea una nueva razon de parada.
    """

    if request.method == 'GET':
        razonesparada = RazonParada.objects.all()
        serializer = RazonParadaSerializer(razonesparada, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            razonparada = RazonParada.objects.get(id_compania=data.get('id_compania'), 
                                                  id_sede = data.get('id_sede'), 
                                                  id_planta = data.get('id_planta'),
                                                  id_razon_parada = data.get('id_razon_parada'))

            idlehs = IdleReasonHostSystem.objects.get(id_compania=data.get('id_compania'), 
                                                  id_sede = data.get('id_sede'), 
                                                  id_planta = data.get('id_planta'),
                                                  id_razon_parada = data.get('id_razon_parada'))
                                                                                        
            return Response(('The given reason code already exist'), status=status.HTTP_302_FOUND)
        except ( RazonParada.DoesNotExist, IdleReasonHostSystem.DoesNotExist) as e:
            serializer = RazonParadaSerializer(data=data)
            serializer_irhs = IdleReasonHostSystemSerializer(data=data)
            if serializer.is_valid() and serializer_irhs.is_valid():
                try:
                    razonparada = serializer.save()
                    idlehs = serializer_irhs.save()
                    serializer_output = IdleReasonHostSystemOuputSerializer(idlehs)
                    content = JSONRenderer().render(serializer_output.data)
                    logger.info(content)
                    url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
                    url = url + defaults.CONTEXT_ROOT + '/'
                    url = url + 'ReasonCode' + '/' + str( idlehs.id )
                    r = requests.put(url, data = content)
                    if (r.status_code == 204):
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        # TODO: BORRAR LAS ENTRADAS.
                        return Response(r.text, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except requests.exceptions.RequestException as e:
                    logger.error(e)
                    return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                logger.error(serializer.errors)
                logger.error(serializer_irhs.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated, ))
@parser_classes((JSONParser,))
def razon_parada_detail(request, pk, format=None):
    """
    Obtiene, actualiza or borra una razon de parada.
    """

    try:
        data = JSONParser().parse(request)
        razonparada = RazonParada.objects.get(id_compania=data.get('id_compania'), 
                                                  id_sede = data.get('id_sede'), 
                                                  id_planta = data.get('id_planta'),
                                                  id_razon_parada = data.get('id_razon_parada'))
        idlehs = IdleReasonHostSystem.objects.get(id_compania=data.get('id_compania'), 
                                                  id_sede = data.get('id_sede'), 
                                                  id_planta = data.get('id_planta'),
                                                  id_razon_parada = data.get('id_razon_parada'))
                                                  
    except (RazonParada.DoesNotExist, IdleReasonHostSystem.DoesNotExist) :
        if request.method == 'DELETE':
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RazonParadaSerializer(razonparada)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RazonParadaSerializer(razonparada, data=data)
        serializer_irhs = IdleReasonHostSystemSerializer(idlehs, data=data)
        if serializer.is_valid():
            if serializer_irhs.is_valid():
                try:
                    serializer.save()
                    serializer_irhs.save()
                    content = JSONRenderer().render(serializer_irhs.data)
                    url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
                    url = url + defaults.CONTEXT_ROOT + '/'
                    url = url + 'ReasonCode' + '/' + str(serializer_irhs.data.get('id') )
                    r = requests.put(url, data = content)
                    if (r.status_code == 204):
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        # TODO: BORRAR LAS ENTRADAS.
                        return Response(r.text, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except requests.exceptions.RequestException as e:
                    logger.error(e)
                    return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                logger.error(serializer_irhs.errors)            
                return Response(serializer_irhs.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.error(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        serializer = RazonParadaSerializer(razonparada)
        try:
            idlereasonserializer = IdleReasonHostSystemOuputSerializer(idlehs)
            content = JSONRenderer().render(idlereasonserializer.data)
            url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
            url = url + defaults.CONTEXT_ROOT + '/'
            url = url + 'ReasonCode' + '/' + str(idlehs.id)
            logger.info('calling url:' + url)
            r = requests.delete(url, data = content)
            if (r.status_code == 204):
                razonparada.delete()
                idlehs.delete()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(r.text, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.exceptions.RequestException as e:
            logger.error(e)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
@parser_classes((JSONParser,))
def grupo_maquina_list(request, format=None):
    """
    Lista todas los grupos de maquina, or crea un nuevo grupo de maquina.
    """
   
    if request.method == 'GET':
        grupomaquina = GrupoMaquina.objects.all()
        serializer = GrupoMaquinaSerializer(grupomaquina, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            grupomaquina = GrupoMaquina.objects.get(id_compania=data.get('id_compania'), 
                                                    id_sede = data.get('id_sede'), 
                                                    id_planta = data.get('id_planta'),
                                                    id_grupo_maquina = data.get('id_grupo_maquina'))
            return Response(status=status.HTTP_302_FOUND)
        except GrupoMaquina.DoesNotExist:
            serializer = GrupoMaquinaSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.error(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated, ))
@parser_classes((JSONParser,))
def grupo_maquina_detail(request, pk, format=None):
    """
    Obtiene, actualiza or borra un grupo de maquina.
    """

    try:
        data = JSONParser().parse(request)
        grupomaquina = GrupoMaquina.objects.get(id_compania=data.get('id_compania'), 
                                                    id_sede = data.get('id_sede'), 
                                                    id_planta = data.get('id_planta'),
                                                    id_grupo_maquina = data.get('id_grupo_maquina'))
    except GrupoMaquina.DoesNotExist:
        if request.method == 'DELETE':
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GrupoMaquinaSerializer(grupomaquina)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        serializer = GrupoMaquinaSerializer(grupomaquina, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        grupomaquina.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
@parser_classes((JSONParser,))
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
            return Response(status=status.HTTP_302_FOUND)
        except Maquina.DoesNotExist:
            serializer_p = MaquinaSerializer(data=data)
            serializer_mhs = MachineHostSystemSerializer(data=data)
            if serializer_p.is_valid() and serializer_mhs.is_valid():
                serializer_p.save()
                serializer_mhs.save()
                return Response(serializer_p.data, status=status.HTTP_201_CREATED)
            else:
                logger.error(serializer_p.errors)
                logger.error(serializer_mhs.errors)
                return Response(serializer_p.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated, ))
@parser_classes((JSONParser,))
def maquina_detail(request, pk, format=None):
    """
    Obtiene, actualiza or borra una maquina.
    """

    try:
        data = JSONParser().parse(request)
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

    except ( Maquina.DoesNotExist, MachineHostSystem.DoesNotExist) as e:
        if request.method == 'DELETE':
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MaquinaSerializer(maquina)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MaquinaSerializer(maquina, data=data)
        serializer_mhs = MachineHostSystemSerializer( machinehs, data=data)
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
@parser_classes((JSONParser,))
def plan_produccion_list(request, format=None):
    """
    Lista todos los planes de produccion, or crea un nuevo plan de produccion.
    """

    if request.method == 'GET':
        planproduccion = PlanProduccion.objects.all()
        serializer = PlanProduccionSerializer(planproduccion, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            planproduccion = PlanProduccion.objects.get(id_compania = data.get('id_compania'),
                                           id_sede = data.get('id_sede'),
                                            id_planta = data.get('id_planta'),
                                             id_grupo_maquina = data.get('id_grupo_maquina'),
                                              id_maquina = data.get('id_maquina'),
                                               ano = data.get('ano'),
                                                mes = data.get('mes'))
            return Response(status=status.HTTP_302_FOUND)
        except PlanProduccion.DoesNotExist:
            serializer = PlanProduccionSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated, ))
@parser_classes((JSONParser,))
def plan_produccion_detail(request, pk, format=None):
    """
    Obtiene, actualiza or borra un plan de produccion.
    """

    try:
        data = JSONParser().parse(request)
        planproduccion = PlanProduccion.objects.get(id_compania = data.get('id_compania'),
                                           id_sede = data.get('id_sede'),
                                            id_planta = data.get('id_planta'),
                                             id_grupo_maquina = data.get('id_grupo_maquina'),
                                              id_maquina = data.get('id_maquina'),
                                               ano = data.get('ano'),
                                                mes = data.get('mes'))
    except PlanProduccion.DoesNotExist:
        if request.method == 'DELETE':
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PlanProduccionSerializer(planproduccion)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PlanProduccionSerializer(planproduccion, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        planproduccion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
@parser_classes((JSONParser,))
def orden_produccion_planeada_list(request, format=None):
    """
    Lista todos las ordenes de produccion planeada, or crea una nueva orden de produccion planeada.
    """

    if request.method == 'GET':
        ordenproduccionplaneada = OrdenProduccionPlaneada.objects.all()
        serializer = OrdenProduccionPlaneadaSerializer(ordenproduccionplaneada, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        try:

            print (OrdenProduccionPlaneada.objects.filter(id_compania = data.get('id_compania'),
                                           id_sede = data.get('id_sede'),
                                            id_planta = data.get('id_planta'),
                                             id_grupo_maquina = data.get('id_grupo_maquina'),
                                              id_maquina = data.get('id_maquina'),
                                               ano = data.get('ano'),
                                                mes = data.get('mes'),
                                                 id_produccion = data.get('id_produccion')).query)

            ordenproduccionplaneada = OrdenProduccionPlaneada.objects.get(id_compania = data.get('id_compania'),
                                           id_sede = data.get('id_sede'),
                                            id_planta = data.get('id_planta'),
                                             id_grupo_maquina = data.get('id_grupo_maquina'),
                                              id_maquina = data.get('id_maquina'),
                                               ano = data.get('ano'),
                                                mes = data.get('mes'),
                                                 id_produccion = data.get('id_produccion'))

            return Response(status=status.HTTP_302_FOUND)
        except OrdenProduccionPlaneada.DoesNotExist:
            serializer = OrdenProduccionPlaneadaSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.error(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated, ))
@parser_classes((JSONParser,))
def orden_produccion_planeada_detail(request, pk, format=None):
    """
    Obtiene, actualiza or borra una order de produccion planeada.
    """

    try:
        data = JSONParser().parse(request)
        ordenproduccionplaneada = OrdenProduccionPlaneada.objects.get(id_compania = data.get('id_compania'),
                                           id_sede = data.get('id_sede'),
                                            id_planta = data.get('id_planta'),
                                             id_grupo_maquina = data.get('id_grupo_maquina'),
                                              id_maquina = data.get('id_maquina'),
                                               ano = data.get('ano'),
                                                mes = data.get('mes'),
                                                 id_produccion = data.get('id_produccion'))

    except OrdenProduccionPlaneada.DoesNotExist:
        if request.method == 'DELETE':
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrdenProduccionPlaneadaSerializer(ordenproduccionplaneada)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = OrdenProduccionPlaneadaSerializer(ordenproduccionplaneada, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        ordenproduccionplaneada.delete()
        # If the job was running, then the system should stop it.
        dict = { 'company' : data.get('id_compania'), 
                'location' : data.get('id_sede'),
                'plant' : data.get('id_planta'),
                'machineGroup' : data.get('id_grupo_maquina'),
                'machineId' : data.get('id_maquina'),
                'year' : data.get('ano'),
                'month' : data.get('mes') ,
                'activityType' : 'E', 
                'stopReason': '',
                'productionOrder' : data.get('id_produccion') }
        jsonText = json.dumps(dict)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'Register/ActivityRegister' 
        try:
            r = requests.put(url, data = json_data)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except requests.exceptions.RequestException as e:
            logger.error(e)
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
@parser_classes((JSONParser,))
def parada_planeada_list(request, format=None):
    """
    Lista todos las paradas planeadas, or crea una nueva parada planeada.
    """

    if request.method == 'GET':
        paradaplaneada = ParadaPlaneada.objects.all()
        serializer = ParadaPlaneadaSerializer(paradaplaneada, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            paradaplaneada = ParadaPlaneada.objects.get(id_compania = data.get('id_compania'),
                                           id_sede = data.get('id_sede'),
                                            id_planta = data.get('id_planta'),
                                             id_grupo_maquina = data.get('id_grupo_maquina'),
                                              id_maquina = data.get('id_maquina'),
                                               ano = data.get('ano'),
                                                mes = data.get('mes'))
            return Response(status=status.HTTP_302_FOUND)
        except ParadaPlaneada.DoesNotExist:
            serializer = ParadaPlaneadaSerializer(data=data)
            if serializer.is_valid():
               serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated, ))
@parser_classes((JSONParser,))
def parada_planeada_detail(request, pk, format=None):
    """
    Obtiene, actualiza or borra una parada planeada.
    """

    try:
        data = JSONParser().parse(request)
        paradaplaneada = ParadaPlaneada.objects.get(id_compania = data.get('id_compania'),
                                           id_sede = data.get('id_sede'),
                                            id_planta = data.get('id_planta'),
                                             id_grupo_maquina = data.get('id_grupo_maquina'),
                                              id_maquina = data.get('id_maquina'),
                                               ano = data.get('ano'),
                                                mes = data.get('mes'))
    except ParadaPlaneada.DoesNotExist:
        if request.method == 'DELETE':
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ParadaPlaneadaSerializer(paradaplaneada)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ParadaPlaneadaSerializer(paradaplaneada, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        paradaplaneada.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListActivityRegisterView(ListView):

    model = ActivityRegister
    template_name = 'ActivityRegister_list.html'


def ordenes_from_maquina(request):
    _id_compania =request.GET.get('id_compania')
    _id_sede=request.GET.get('id_sede')
    _id_planta=request.GET.get('id_planta')
    _id_grupo_maquina=request.GET.get('id_grupo_maquina')
    _id_maquina=request.GET.get('id_maquina')
    _ano=request.GET.get('ano')
    _mes=request.GET.get('mes')
    
    ret=[]
    sqlText = "SELECT f.id, f.id_produccion \
		FROM canonical_maquina e, canonical_grupomaquina a, canonical_compania b, canonical_sede c, canonical_planta d, canonical_ordenproduccionplaneada f \
	       WHERE b.id = %s AND c.id = %s AND d.id = %s AND a.id = %s AND e.id = %s AND f.ano = %s AND f.mes = %s \
                 AND c.id_compania = b.id_compania AND d.id_compania = c.id_compania AND d.id_sede = c.id_sede \
		 AND a.id_compania = d.id_compania AND a.id_sede = d.id_sede AND a.id_planta = d.id_planta \
		 AND e.id_compania = a.id_compania AND e.id_sede = a.id_sede AND e.id_planta = a.id_planta \
		 AND e.id_grupo_maquina = a.id_grupo_maquina AND f.id_compania = e.id_compania AND f.id_sede = e.id_sede \
		 AND f.id_planta = e.id_planta AND f.id_grupo_maquina = e.id_grupo_maquina AND f.id_maquina = e.id_maquina"

    if _id_maquina:
        all_Orders = OrdenProduccionPlaneada.objects.raw(sqlText, [_id_compania, _id_sede, _id_planta, _id_grupo_maquina, _id_maquina, _ano, _mes] ) 
        for order in all_Orders:
            ret.append(dict(id=order.id, value=order.id_produccion))

    if len(ret)!=1:
        ret.insert(0, dict(id='', value='---'))
    return HttpResponse(json.dumps(ret), 
              content_type='application/json')


def maquinas_from_group(request):
    _id_compania =request.GET.get('id_compania')
    _id_sede=request.GET.get('id_sede')
    _id_planta=request.GET.get('id_planta')
    _id_grupo_maquina=request.GET.get('id_grupo_maquina')
    ret=[]
    if _id_grupo_maquina:
        all_gMaquina = Maquina.objects.raw("SELECT e.id, e.descr \
			  FROM canonical_maquina e, canonical_grupomaquina a, canonical_compania b, canonical_sede c, canonical_planta d \
			 WHERE b.id = %s AND c.id = %s AND d.id = %s AND a.id = %s \
			   AND c.id_compania = b.id_compania AND d.id_compania = c.id_compania \
			   AND d.id_sede = c.id_sede AND a.id_compania = d.id_compania \
			   AND a.id_sede = d.id_sede AND a.id_planta = d.id_planta \
			   AND e.id_compania = a.id_compania AND e.id_sede = a.id_sede \
			   AND e.id_planta = a.id_planta AND e.id_grupo_maquina = a.id_grupo_maquina", [_id_compania, _id_sede, _id_planta, _id_grupo_maquina] )
        for maquina in all_gMaquina:
            ret.append(dict(id=maquina.id, value=maquina.descr))

    if len(ret)!=1:
        ret.insert(0, dict(id='', value='---'))
    return HttpResponse(json.dumps(ret), 
              content_type='application/json')


class ActivityRegisterForm(ModelForm):
    id_maquina=forms.ModelChoiceField(Maquina.objects.none())
    id_produccion=forms.ModelChoiceField(OrdenProduccionPlaneada.objects.none())
    class Meta:
        model = ActivityRegister
        fields = ['id_compania', 'id_sede', 'id_planta', 'id_grupo_maquina', 'id_maquina', 'ano', 'mes', 'tipo_actividad', 'id_razon_parada', 'id_produccion']

    def grupo_maquina_for_choice_field(self, available_choices):
        all_gMaquina = GrupoMaquina.objects.raw("SELECT a.id, a.descr \
						   FROM canonical_grupomaquina a, canonical_compania b, canonical_sede c, canonical_planta d \
						  WHERE b.id = %s \
						    AND c.id = %s \
						    AND d.id = %s \
						    AND c.id_compania = b.id_compania \
						    AND d.id_compania = c.id_compania \
						    AND d.id_sede = c.id_sede \
					    	    AND a.id_compania = d.id_compania \
						    AND a.id_sede = d.id_sede \
						    AND a.id_planta = d.id_planta", [self.id_compania, self.id_sede, self.id_planta] )

        for gMaquina in all_gMaquina:
            available_choices.append((gMaquina.id, gMaquina.descr))

    def razones_parada_for_choice_field(self, available_choices):
        all_rParada = RazonParada.objects.raw("SELECT a.id, a.descr \
						   FROM canonical_razonparada a, canonical_compania b, canonical_sede c, canonical_planta d \
						  WHERE b.id = %s \
						    AND c.id = %s \
						    AND d.id = %s \
						    AND c.id_compania = b.id_compania \
						    AND d.id_compania = c.id_compania \
						    AND d.id_sede = c.id_sede \
					    	    AND a.id_compania = d.id_compania \
						    AND a.id_sede = d.id_sede \
						    AND a.id_planta = d.id_planta", [self.id_compania, self.id_sede, self.id_planta] )

        for rParada in all_rParada:
            available_choices.append((rParada.id, rParada.descr))

    def __init__(self, request, *args, **kwargs):
        if 'initial' in kwargs:
            initial_values = kwargs.get('initial')
            id_compania = initial_values['id_compania'] 
            id_sede = initial_values['id_sede'] 
            id_planta = initial_values['id_planta']
        else:
            id_compania = None
            id_sede = None
            id_planta = None

        super(ActivityRegisterForm, self).__init__(*args, **kwargs)

        self.fields['id_compania'].widget.attrs['readonly'] = True
        self.fields['id_sede'].widget.attrs['readonly'] = True
        self.fields['id_planta'].widget.attrs['readonly'] = True

        # Save in the form default values.
        self.id_compania = id_compania
        self.id_sede = id_sede
        self.id_planta = id_planta

        # Set posible values for the field grupo maquina.
        gMaquina_choices = []
        rParada_choices = []
        self.grupo_maquina_for_choice_field(gMaquina_choices)
        self.razones_parada_for_choice_field(rParada_choices)
        self.fields['id_grupo_maquina'] = forms.ChoiceField(choices=gMaquina_choices)
        self.fields['id_razon_parada'] = forms.ChoiceField(choices=rParada_choices)


class CreateRegisterView(LoginRequiredMixin, CreateView):

    model = ActivityRegister
    template_name = 'ActivityRegister_edit.html'
    fields = '__all__'
               
    def getDefaults(self, user):
        initial = {}
        print("userid:" + str(user.id))
        employeeData = Employee.objects.get(user_id=user.id)
        initial ['id_compania'] = employeeData.id_compania
        initial ['id_sede'] = employeeData.id_sede
        initial ['id_planta'] = employeeData.id_planta
        initial ['author'] = user.id
        now = datetime.datetime.now()
        initial ['ano'] = now.year
        initial ['mes'] = now.month
        return initial
   
    def form_valid(self, form):
        self.object = form.save()
        serializer = DisplayDeviceSerializer(self.object)
        content = JSONRenderer().render(serializer.data)
        #async(putActivityRegister, content)
        return HttpResponseRedirect(self.get_success_url())    

    # if a GET (or any other method) we'll create a blank form
    def get(self, request, *args, **kwargs):
        initial = self.getDefaults(request.user)
        form = ActivityRegisterForm(request, initial=initial)
        return render(request, self.template_name, {'form': form})

    def get_success_url(self):
        return reverse('activity-register-list-view')

def reports(request,report):
    template_report = {
        "1":"var_evolution_report.html",
        "2":"downtime_reasons.html"
        }
    return render(request,template_report[report], {})

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSeralizer
    permission_classes = (IsAuthenticated,)

class SedeByCompaniaId(APIView):
    """
    Get a Sede by companiaId.
    """
    def get(self, request, format=None):
        sedes = Sede.objects.filter(id_compania= request.GET.get('compania', None))
        print(request)
        serializer =  SedeSerializer(sedes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MaquinaByGrupoId(APIView):
    """
    Get a Maquina by companiaId.
    """
    def get(self, request, format=None):
        maquinas = Maquina.objects.filter(id_grupo_maquina= request.GET.get('grupo', None))
        print(request)
        serializer =  MaquinaSerializer(maquinas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GruposMaquinaByPlantaId(APIView):
    """
    Get Grupos Maquinas by companiaId.
    """
    def get(self, request, format=None):
        grupos_maquinas = GrupoMaquina.objects.filter(id_planta= request.GET.get('planta', None))
        serializer =  GrupoMaquinaSerializer(grupos_maquinas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PlantaBySedeId(APIView):
    """
    Get Plantas by companiaId.
    """
    def get(self, request, format=None):
        plantas = Planta.objects.filter(id_sede= request.GET.get('sede', None))
        serializer =  PlantaSerializer(plantas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
