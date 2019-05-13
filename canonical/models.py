from django.db import models
import datetime
from django.contrib.auth.models import User


# Create your models here.

class Compania(models.Model):
    id_compania = models.CharField(max_length=60)
    descr = models.CharField(max_length=200)
    create_date = models.DateTimeField('create datetime',  auto_now=False,  auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)

    def __str__(self):
        return self.id_compania + ' ' + self.descr

class Sede(models.Model):
    id_compania = models.CharField(max_length=60) 
    id_sede = models.CharField(max_length=60)
    descr =  models.CharField(max_length=200)
    create_date = models.DateTimeField('create datetime',  auto_now=False,  auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)

    def __str__(self):
        return self.id_sede + ' ' + self.descr

class Planta(models.Model):
    id_compania = models.CharField(max_length=60)
    id_sede = models.CharField(max_length=60)
    id_planta = models.CharField(max_length=60)
    descr =  models.CharField(max_length=200)
    create_date = models.DateTimeField('create datetime',  auto_now=False,  auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)

    def __str__(self):
        return self.id_planta + ' ' + self.descr

class RazonParada(models.Model):
    id_compania = models.CharField(max_length=60)
    id_sede = models.CharField(max_length=60)
    id_planta = models.CharField(max_length=60)
    id_razon_parada = models.CharField(max_length=60)
    descr =  models.CharField(max_length=200)
    grupo_razon_parada = models.CharField(max_length=60)
    causa_raiz_parada =  models.CharField(max_length=60)
    afecta_capacidad = models.CharField(max_length=1)
    clasificacion = models.CharField(max_length=1, default='0')
    create_date = models.DateTimeField('create datetime',  auto_now=False,  auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)

    def __str__(self):
        return self.id_razon_parada + ' ' + self.descr

class GrupoMaquina(models.Model):
    id_compania = models.CharField(max_length=60)
    id_sede = models.CharField(max_length=60)
    id_planta = models.CharField(max_length=60)
    id_grupo_maquina = models.CharField(max_length=60)
    descr =  models.CharField(max_length=200)
    create_date = models.DateTimeField('create datetime',  auto_now=False,  auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)

    def __str__(self):
        return self.id_grupo_maquina + ' ' + self.descr

class Maquina(models.Model):
    id_compania = models.CharField(max_length=60)
    id_sede = models.CharField(max_length=60)
    id_planta = models.CharField(max_length=60)
    id_grupo_maquina = models.CharField(max_length=60)
    id_maquina = models.CharField(max_length=60)
    descr = models.CharField(max_length=200)
    estado_actual = models.CharField(max_length=2)
    tasa_vel_esperada = models.FloatField(default=0)
    tiempo_esperado_config = models.FloatField(default=0)
    factor_conversion_kg_ciclo = models.FloatField(default=0)
    factor_conversion_mil_ciclo = models.FloatField(default=0)
    factor_conversion_emp_ciclo = models.FloatField(default=0)
    descripcion_sin_trabajo = models.CharField(max_length=200,
                                                default= 'sin_trabajo')
    create_date = models.DateTimeField('create datetime',  auto_now=False,  auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)
    tiempo_refresco = models.IntegerField(default=5)

    def __str__(self):
        return self.id_maquina + ' ' + self.descr

class PlanProduccion(models.Model):
    YEAR_CHOICES = []
    for r in range(1980, (datetime.datetime.now().year+1)):
        YEAR_CHOICES.append((r,r))

    MONTH_CHOICES = []
    for m in range(1,12):
        MONTH_CHOICES.append((m,m))

    id_compania = models.CharField(max_length=60)
    id_sede = models.CharField(max_length=60)
    id_planta = models.CharField(max_length=60)
    id_grupo_maquina = models.CharField(max_length=60)
    id_maquina = models.CharField(max_length=60)
    ano = models.IntegerField('ano', choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    mes = models.IntegerField('mes', choices=MONTH_CHOICES, default=datetime.datetime.now().month)
    create_date = models.DateTimeField('create datetime',  auto_now=False,  auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)

class OrdenProduccionPlaneada(models.Model):
    id_compania = models.CharField(max_length=60)
    id_sede = models.CharField(max_length=60)
    id_planta = models.CharField(max_length=60)
    id_grupo_maquina = models.CharField(max_length=60)
    id_maquina = models.CharField(max_length=60)
    ano = models.IntegerField()
    mes = models.IntegerField()
    id_produccion = models.CharField(max_length=30)
    id_articulo = models.CharField(max_length=30)
    descr_articulo = models.CharField(max_length=120)
    fechahora_inicial = models.DateTimeField()
    fechahora_final =  models.DateTimeField()
    num_horas = models.IntegerField()
    cantidad_producir= models.FloatField()
    tasa_esperada = models.FloatField()
    velocidad_esperada = models.FloatField()
    create_date = models.DateTimeField('create datetime',  auto_now=False,  auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)
    
class ParadaPlaneada(models.Model):
    id_compania = models.CharField(max_length=60)
    id_sede = models.CharField(max_length=60)
    id_planta = models.CharField(max_length=60)
    id_grupo_maquina = models.CharField(max_length=60)
    id_maquina = models.CharField(max_length=60)
    ano = models.IntegerField()
    mes = models.IntegerField()
    fechahora_inicial = models.DateTimeField('fecha hora inicio')
    fechahora_final =  models.DateTimeField('fecha hora fin')
    create_date = models.DateTimeField('create datetime',  auto_now=False,  auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)

class ActivityRegister(models.Model):
    ACTIVITY_TYPE = (
        ('S', 'Comienzo Orden de Produccion'),
        ('E', 'Fin Orden de Produccion'),
        ('C', 'Comienzo de Parada'),
        ('F', 'Fin de Parada'),
    )
    id_compania = models.CharField(max_length=60)
    id_sede = models.CharField(max_length=60)
    id_planta = models.CharField(max_length=60)
    id_grupo_maquina = models.CharField(max_length=60)
    id_maquina =  models.CharField(max_length=60)
    ano = models.IntegerField()
    mes = models.IntegerField()
    tipo_actividad = models.CharField(max_length=1, choices=ACTIVITY_TYPE, default='S')
    id_razon_parada = models.CharField(max_length=60)
    id_produccion = models.CharField(max_length=30)
    author = models.IntegerField(null=True, blank=True)    
    create_date =  models.DateTimeField('create datetime',  auto_now=False,  auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)


