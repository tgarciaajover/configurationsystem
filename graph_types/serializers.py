from rest_framework import serializers
from graph_types.models import GraphType

class GraphTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraphType
        fields = '__all__'