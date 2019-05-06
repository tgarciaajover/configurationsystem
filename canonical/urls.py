from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from canonical import views
from rest_framework import routers
from rest_framework.authtoken.views import ObtainAuthToken
from django.conf.urls import *
from canonical.views import UserViewSet
from canonical.views import SedeByCompaniaId, MaquinaByGrupoId, GruposMaquinaByPlantaId, PlantaBySedeId

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
    url('sede_compania', SedeByCompaniaId.as_view(), name='sede_by_compania_id'),
    url('maquina_grupo_maquina', MaquinaByGrupoId.as_view(), name='maquina_by_grupo_id'),
    url('grupo_maquina_planta', GruposMaquinaByPlantaId.as_view(), name='grupo_maquina_by_planta_id'),
    url('planta_compania', PlantaBySedeId.as_view(), name='planta_by_sede_id'),
    url('arbol', views.arbol, name='arbol'),
    url('variables_comunes', views.variables_comunes, name='variables_comunes'),
    url('maquinas_variables', views.maquinas_variables, name='maquinas_variables'),
]

#urlpatterns = format_suffix_patterns(urlpatterns)
