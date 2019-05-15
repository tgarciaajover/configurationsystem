from django.db import models
import datetime
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from django.utils.six import python_2_unicode_compatible
import common.models as common
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
    create_date = models.DateTimeField('create datetime',  auto_now=False,  auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)


class Operator(common.AuditedModel):
    IDENTIFICATION_TYPE = (
        ('C', 'Cedula'),
        ('P', 'Pasaporte',),
        ('E', 'Cedula de Extranjeria'),
        ('T', 'Tarjeta de Identidad'),
        ('U', 'Registro Civil'),
        ('D', 'Carnet Diplomatico'),
        ('O', 'TI2')
    )
    first_name = models.CharField(max_length=120)
    second_name = models.CharField(max_length=120, null=True, blank=True)
    other_names = models.CharField(max_length=120, null=True, blank=True)
    surname = models.CharField(max_length=120)
    second_last_name = models.CharField(max_length=120, null=True, blank=True)
    other_surnames = models.CharField(max_length=120, null=True, blank=True)
    email = models.EmailField(max_length=200)
    address = models.CharField(max_length=300, null=True)
    phone = models.CharField(max_length=150, blank=True)
    identification_type = models.CharField(max_length=2, choices=IDENTIFICATION_TYPE, null=True, blank=True)
    identification = models.CharField(max_length=20, null=True, blank=True)
    user = models.OneToOneField(User, related_name='person')

    active_account = models.BooleanField(default=True)

    history = HistoricalRecords()

    class Meta:
        unique_together = ('identification_type', 'identification', 'user')

    def __unicode__(self):
        return "{}-{}".format(self.get_identification_type_display(), self.identification)


class ThirdParty(common.AuditedModel):
    visible_name = models.CharField(max_length=200)

    history = HistoricalRecords()

    def __str__(self):
        return self.visible_name


class Phone(common.AuditedModel):
    ROL_PHONE = (
        ('M', 'Main'),
        ('S', 'Secondary'),
    )
    third_part = models.ForeignKey(ThirdParty, on_delete=models.CASCADE)
    country_code = models.CharField(max_length=2)
    city_code = models.CharField(max_length=1)
    number = models.CharField(max_length=10)
    rol = models.CharField(max_length=2, choices=ROL_PHONE, null=True, blank=True)

    history = HistoricalRecords()


class Email(common.AuditedModel, common.ValidModel):
    ROL_EMAIL = (
        ('M', 'Main'),
        ('S', 'Secondary'),
    )
    third_party = models.ForeignKey(ThirdParty, on_delete=models.CASCADE)
    email = models.EmailField(max_length=200)
    rol = models.CharField(max_length=2, choices=ROL_EMAIL, null=True, blank=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "Emails"

@python_2_unicode_compatible
class Department(models.Model):
    department_dane_code = models.CharField(max_length=2)
    name = models.CharField(max_length=60, null=True)

    class Meta:
        """Meta."""

        verbose_name = "Departament"
        verbose_name_plural = "Departaments"

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Municipality(models.Model):
    municipality_dane_code = models.CharField(max_length=5, null=True)
    departament = models.ForeignKey(Department, related_name='departament', on_delete=models.PROTECT)
    name = models.CharField(max_length=60, null=True)

    class Meta:
        """Meta."""

        verbose_name = "Municipality"
        verbose_name_plural = "Municipalities"

    def __str__(self):
        return self.name

class UrbanDirectionColombia():
    VIA_TYPE = (
        ('AU', 'Freeway'),
        ('AV', 'Avenue'),
        ('AC', 'Avenue Street'),
        ('AK', 'Avenue Carrera'),
        ('BL', 'Boulevard'),
        ('CL', 'Street'),
        ('KR', 'Carrera'),
        ('CT', 'Highway'),
        ('CQ', 'Peripheral'),
        ('CV', 'Encircle'),
        ('DG', 'Diagonal'),
        ('PJ', 'Passage'),
        ('PS', 'Walk'),
        ('PT', 'Pedestrian'),
        ('TV', 'Transversal'),
        ('TC', 'Trunk'),
        ('VT', 'Variant'),
        ('VI', 'Vía')
    )

    QUADRANT = (
        ('S', 'South'),
        ('N', 'North'),
        ('E', 'East'),
        ('W', 'West')
    )

    PREFIX = (
        ('B', 'BIS'),
    )

    ADDRESS_ADD_ON = (
        ('AD', 'ADMINISTRATION'),
        ('AG', 'AGRUPATION'),
        ('AL', 'LOFT'),
        ('AP', 'APARTAMENT'),
        ('BR', 'NEIGHBORHOOD'),
        ('BQ', 'BLOCK'),
        ('BG', 'CELLAR'),
        ('CS', 'HOUSE'),
        ('CU', 'CELL'),
        ('CE', 'MALL'),
        ('CD', 'CITADEL'),
        ('CO', 'RESIDENTIAL'),
        ('CN', 'CONSULTING_ROOM'),
        ('DP', 'DEPOSIT'),
        ('DS', 'BASEMENT_DEPOSIT'),
        ('ED', 'BUILDING'),
        ('EN', 'ENTRANCE'),
        ('EQ', 'CORNER'),
        ('ES', 'STATION'),
        ('ET', 'STAGE'),
        ('EX', 'EXTERIOR'),
        ('FI', 'ESTATE'),
        ('GA', 'GARAGE'),
        ('GS', 'BASEMENT_GARAGE'),
        ('IN', 'INTERIOR'),
        ('KM', 'KILOMETER'),
        ('LC', 'LOCAL'),
        ('LM', 'MEZZANINE_LOCAL'),
        ('LT', 'LOT'),
        ('MZ', 'APPlE'),
        ('MN', 'MEZZANINE'),
        ('MD', 'MODULE'),
        ('OF', 'OFFICE'),
        ('PQ', 'PARK'),
        ('PA', 'PARKING_LOT'),
        ('PN', 'PENT_HOUSE'),
        ('PI', 'FLOOR'),
        ('PL', 'LEVEL'),
        ('PR', 'PORTERIA'),
        ('PD', 'PREDIO'),
        ('PU', 'POST'),
        ('RP', 'ROUND POINT'),
        ('SC', 'SECTOR'),
        ('SS', 'SEMISOTANO'),
        ('SO', 'BASEMENT'),
        ('ST', 'SUITE'),
        ('SM', 'SUPERMANZANA'),
        ('TZ', 'TERRACE'),
        ('TO', 'TOWER'),
        ('UN', 'UNIT'),
        ('UL', 'RESIDENCIAL_UNIT'),
        ('UR', 'URBANIZATION'),
        ('ZN', 'ZONE')
    )

    ADDRESS_TYPE = (
        ('N', 'National'),
        ('E', 'Exterior'),
    )

    address_type = models.CharField(max_length=2, choices=ADDRESS_TYPE, null=True, blank=True, default='N')
    via_type = models.CharField(max_length=2, choices=VIA_TYPE, help_text="Tipe of via, ej: Avenida")
    main_via = models.CharField('Número/Nombre', max_length=30, help_text="Number or name common main via, ej: Esperanza")
    letter_main_via = models.CharField(max_length=3, null=True, blank=True, help_text="Letters assosiated to the main via")
    quadrant_main_via = models.CharField(max_length=1, choices=QUADRANT, null=True, blank=True, help_text="(North, South, East, West)")
    generator_via = models.CharField(max_length=30, help_text="Number or common generator via name, eg: 62")
    letter_generator_via = models.CharField(max_length=3, null=True, blank=True, help_text="Letters assosiated to the generator via")
    prefix_generator_via = models.CharField("Prefix", max_length=1, choices=PREFIX, null=True, blank=True, help_text="Via generator sufix, eg: Bis")
    prefix_letter_generator_via = models.CharField(max_length=3, null=True, blank=True, help_text="Letter that accompanies the suffix")
    number_plate = models.CharField(max_length=2, help_text="Plate, eg: 49")
    quadrant_generator_via = models.CharField("Quadrant", max_length=1, choices=QUADRANT, null=True, blank=True, help_text="(North, South, East, West)")
    complement = models.CharField(max_length=2, choices=ADDRESS_ADD_ON, null=True, blank=True)
    departament = models.ForeignKey(Department)
    municipality = models.ForeignKey(Municipality)

    class Meta:
        verbose_name_plural = "Addresses in Colombia"

    def __unicode__(self):
        return "{} {} {} {} {} {} {} {} {} {} {}".format(
            self.via_type or "",
            self.main_via or "",
            self.letter_main_via or "",
            self.quadrant_main_via or "",
            self.generator_via or "",
            self.letter_generator_via or "",
            self.prefix_generator_via or "",
            self.prefix_letter_generator_via or "",
            self.number_plate or "",
            self.quadrant_generator_via or "",
            self.complement or ""
        )

class MachineOperator(models.Model):
    operator = models.ForeignKey('Operator', on_delete=models.CASCADE)
    id_compania = models.CharField(max_length=60)
    id_sede = models.CharField(max_length=60)
    id_planta = models.CharField(max_length=60)
    id_grupo_maquina = models.CharField(max_length=60)
    id_maquina = models.CharField(max_length=60)