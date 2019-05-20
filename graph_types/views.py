from django.shortcuts import render
from rest_framework.views import APIView
from graph_types.models import GraphType
from graph_types.serializers import GraphTypeSerializer

from rest_framework.response import Response
from rest_framework import status

# Create your views here.


class GraphTypeList(APIView):
    """
    List all graph types.
    """
    def get(self, request, format=None):
        # Se obtienen todos loes tipos de graficas
        graph_types = GraphType.objects.all()
        # Se serializan los tipos de graficas
        serializer = GraphTypeSerializer(graph_types, many=True)
        # Retorna los tipos de graficas serializadas y status 200.
        return Response(serializer.data, status=status.HTTP_200_OK)
