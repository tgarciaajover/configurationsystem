from django.db import models

from django.contrib.auth.models import User
from graph_types.models import GraphType

# Create your models here.


class Dashboard(models.Model):
    """
        Modelo que maneja los dashboard de los usuarios

        Campos
        ------
        name
            Nombre del dashboard
        layout
            Nombre del layout en el que se encuentra el dashboard
        favorite
            Indica si el dashboard es favorito
        user
            Referencia al usuario al que se encuentra asociado el dashboard
    """
    name = models.CharField(max_length=300, null=False, blank=False)
    layout = models.CharField(max_length=100, null=False, blank=False)
    favorite = models.BooleanField(null=False, blank=False, default=False)
    user = models.ForeignKey( User , on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'dashboards'


class Chart(models.Model):
    """
        Modelo que las graficas que se encuentran asociadas a un dashboard

        Campos
        ------
        graph_type
            Referencia al tipo de grafica
        position
            Posicion en el layout del dashboard en el cual se encuentra la grafica
        kpi_name
            Nombre del KPI asociado a la grafica
        api_url
            Url de la API por la cual se puede acceder a la informacion del KPI
        dashboard
            Referencia al dashboard al cual se encuentra asociado la grafica
    """
    graph_type = models.ForeignKey( GraphType , on_delete=models.CASCADE)
    position = models.IntegerField(blank=False, null=False)
    kpi_name = models.CharField(max_length= 300, blank=False, null=False)
    api_url = models.CharField(max_length= 300, blank=False, null=False)
    dashboard = models.ForeignKey( Dashboard , on_delete=models.CASCADE )

    def __str__(self):
        return str(self.graph_type) + ' ' + str(self.dashboard) + ' ' + self.kpi_name

    class Meta:
        db_table = 'charts'