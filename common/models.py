from django.db import models
from django.contrib.auth import get_user_model
from history.models import HistoricalRecords

# Corresponds to field names not updated during interface processing
black_field_list = ['_state', 'fecha_creacion', 'fecha_actualizacion']

class AuditedModel(models.Model):
    """
        Clase abstracta para auditar los cambios que hacen los usuarios a las clases que

        creado_por_id: Integer
           Id del usuario que creo la instancia
        actualizado_por_id: Integer
           Id del usuario que actualizo por última vez la instancia
        fecha_creación: DateTime
           fecha en que se creo la instancia
        fecha_actualizacion: DateTime
           fecha en que se actualizo por última vez la instancia
    """

    created_by = models.ForeignKey(get_user_model(), related_name="%(app_label)s_%(class)s_created")
    updated_by = models.ForeignKey(get_user_model(), related_name="%(app_label)s_%(class)s_updated")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        abstract = True

class SynchronizableModel(models.Model):
    """
        Clase abstracta para espeficar si una instancia de un modelo debe o no sincronizarse

        last_syncr_dttm: DateTime
           Fecha y hora de la ultima sincronización con la base de datos central

    """
    last_syncr_dttm = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

class ProcessableModel(models.Model):
    """
    Clase abstracta para especificar si un modelo puede o no se incluido en la
    ejecución de una tarea.

    Atributos
    ---------
        instance: Integer
           instance del proceso que puede estar utilizando la definición
        in_process: Boolean
           Indica si la instancia esta siendo utiliza por algún proceso
        thread: BigInteger
           identificador del thread que esta utilizando la instancia

    """
    instance = models.IntegerField(default=0, null=True, blank=True)
    in_process = models.BooleanField(default=False)
    thread = models.BigIntegerField(default=0)

    class Meta:
        abstract = True


class ValidModel(models.Model):
    """
        Clase abstracta que mantiene las fecha entre las cuales una instancia de un modelo es
        valido.

        fecha_inicio_vigencia: DateTime
           fecha en que la instancia esta vigente
        fecha_fin_vigencia: DateTime
           fecha en que la instancia deja de estar vigente

    """
    valid_start_date = models.DateField(auto_now_add=True)
    valid_end_date = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True