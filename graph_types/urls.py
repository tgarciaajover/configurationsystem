from django.conf.urls import url

from graph_types.views import GraphTypeList

# Urls para la app graph_types
urlpatterns = [
    url('graph_types', GraphTypeList.as_view(), name='graph_types'),
]