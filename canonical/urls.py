from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from canonical import views
from rest_framework import routers
from rest_framework.authtoken.views import ObtainAuthToken
from django.conf.urls import *
from canonical.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url('api/auth/', ObtainAuthToken.as_view()),
    url('api/', include(router.urls)),
    url(r'^compania/$', views.compania_list),
    url(r'^compania/(?P<pk>[0-9]+)/$', views.compania_detail),
    url(r'^sede/$', views.sede_list),
    url(r'^sede/(?P<pk>[0-9]+)/$', views.sede_detail),
    url(r'^planta/$', views.planta_list),
    url(r'^planta/(?P<pk>[0-9]+)/$', views.planta_detail),
    url(r'^razon_parada/$', views.razon_parada_list),
    url(r'^razon_parada/(?P<pk>[0-9]+)/$', views.razon_parada_detail),
    url(r'^grupo_maquina/$', views.grupo_maquina_list),
    url(r'^grupo_maquina/(?P<pk>[0-9]+)/$', views.grupo_maquina_detail),
    url(r'^maquina/$', views.maquina_list),
    url(r'^maquina/(?P<pk>[0-9]+)/$', views.maquina_detail),
    url(r'^plan_produccion/$', views.plan_produccion_list),
    url(r'^plan_produccion/(?P<pk>[0-9]+)/$', views.plan_produccion_detail),
    url(r'^orden_produccion_planeada/$', views.orden_produccion_planeada_list),
    url(r'^orden_produccion_planeada/(?P<pk>[0-9]+)/$', views.orden_produccion_planeada_detail),
    url(r'^parada_planeada/$', views.parada_planeada_list),
    url(r'^parada_planeada/(?P<pk>[0-9]+)/$', views.parada_planeada_detail),
]

#urlpatterns = format_suffix_patterns(urlpatterns)
