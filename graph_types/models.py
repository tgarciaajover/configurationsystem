from django.db import models

# Create your models here.


class GraphType(models.Model):
    """
        Modelo que maneja los tipos de graficas disponibles

        Campos
        ------
        name
            Nombre del tipo de graficas
        image_path
            Path de la imagen del tipo de grafica
    """
    name = models.CharField(max_length=200, null=False, blank=False)
    image_path = models.CharField(max_length=300, null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'graph_types'
