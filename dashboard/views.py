from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
import json

from dashboard.models import Dashboard
from dashboard.models import Chart
from django.contrib.auth.models import User

from dashboard.serializers import DashboardSerializer
from dashboard.serializers import ChartSerializer

# Create your views here.

class DashboardsApiView(APIView):
    """
    Retrieve and Create Dashboards.
    """
    def get(self, request, format=None):
        if request.GET.get('user', None):
            user = get_object_or_404(User, username = request.GET.get('user', None))
            dashboards = Dashboard.objects.filter(user=user)
        else:
            # Se obtienen todos los dashboards
            dashboards = Dashboard.objects.all()
        # Se serializan los dashboards
        serializer =  DashboardSerializer(dashboards, many=True)
        # Retorna los dashboards serializados y status 200.

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        # Se obtiene la informacion que viene en el body
        body_data = json.loads(request.body)
        # Se serializa la informacion obtenida del body
        serializer = DashboardSerializer( data = body_data )
        if serializer.is_valid():
            # Agrega el nuevo dashboard
            serializer.save()
            # Retorna el nuevo dashboard y status 200.
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Retorna los errores y status 400 en caso de que la informacion serializada no sea valida.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DashboardDetailApiView(APIView):
    """
        Retrieve, Update and Delete a Dashboard.
    """
    def get(self, request, pk, format=None):
        # Obtiene un dashboard por el id o devuelve status 404
        dashboard = get_object_or_404(Dashboard, id=pk)
        # Serializa un dashboard
        serializer = DashboardSerializer(dashboard)
        # Retorna el dashboard serializado y status 200.
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        # Obtiene un dashboard por el id o devuelve status 404
        dashboard = get_object_or_404(Dashboard, id=pk)
        # Serializa un dashboard
        serializer = DashboardSerializer(dashboard, data=request.data)
        if serializer.is_valid():
            # Guarda el dashboard con los cambios realizados
            serializer.save()
            # Retorna el dashboard serializado y status 200.
            return Response(serializer.data, status.HTTP_200_OK)
        # Retorna los errores y status 400 en caso de que la informacion serializada no sea valida.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        # Obtiene un dashboard por el id o devuelve status 404
        dashboard = get_object_or_404(Dashboard, id=pk)
        # Elimina el dashboard encontrado
        dashboard.delete()
        # Retorna status 204
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChartsApiView(APIView):
    """
        Retrieve and Create Charts.
    """
    def get(self, request, format=None):
        if request.GET.get('dashboard_id', None):
            dashboard = get_object_or_404(Dashboard, id=request.GET.get('dashboard_id', None))
            charts = Chart.objects.filter(dashboard=dashboard)
        else:
            # Se obtienen todas las graficas
            charts = Chart.objects.all()
        # Se serializan todas las graficas
        serializer =  ChartSerializer(charts, many=True)
        # Retorna las graficas serializadas y status 200.
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        # Se obtienen todas las graficas
        body_data = json.loads(request.body)
        # Se serializan todas las graficas
        serializer = ChartSerializer( data = body_data )
        if serializer.is_valid():
            # Guarda la informacion serializada
            serializer.save()
            # Retorna la informacion de la grafica serializada y status 201.
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Retorna los errores y status 400, en caso de que la informacion no sea valida.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChartDetailApiView(APIView):
    """
        Retrieve, Update and Delete a Chart.
    """
    def get(self, request, pk, format=None):
        # Obtiene un chart por el id o devuelve status 404
        chart = get_object_or_404(Chart, id=pk)
        # Serializa un chart
        serializer = ChartSerializer(chart)
        # Retorna el chart serializado y status 200.
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        # Obtiene un chart por el id o devuelve status 404
        chart = get_object_or_404(Chart, id=pk)
        # Serializa un chart
        serializer = ChartSerializer(chart, data=request.data)
        if serializer.is_valid():
            # Guarda el chart con los cambios realizados
            serializer.save()
            # Retorna la informacion serializada y status 200
            return Response(serializer.data, status.HTTP_200_OK)
        # Retorna los errores y status 400 en caso de que la informacion serializada no sea valida
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        # Obtiene un chart por el id o devuelve status 404
        chart = get_object_or_404(Chart, id=pk)
        # Elimina el chart
        chart.delete()
        # Retorna status 204.
        return Response(status=status.HTTP_204_NO_CONTENT)