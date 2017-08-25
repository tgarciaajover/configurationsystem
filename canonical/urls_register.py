from django.conf.urls import url
from canonical import views

urlpatterns = [
    url(r'^add/', views.CreateRegisterView.as_view(), name='activity-register-create-view'),
    url(r'^ajax/maquinas_from_group/$', views.maquinas_from_group, name='maquinas-from-group'),
    url(r'^ajax/ordenes_from_maquina/$', views.ordenes_from_maquina, name='ordenes-from-maquina'),
]

urlpatterns += [
    url(r'^$', views.ListActivityRegisterView.as_view(), name='activity-register-list-view'),
    url(r'^reports/(?P<report>[0-9]+)/$', views.reports),
#(?P<report>[a-zA-Z0-9_])/
]

