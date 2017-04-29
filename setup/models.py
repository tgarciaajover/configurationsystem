from django.db import models
from django.core.exceptions import ValidationError
import setup.defaults as defaults
from xml.etree.ElementTree import Element, tostring
import xml.etree.ElementTree as ET
import requests

# Create your models here.

class SignalType(models.Model):
    name = models.CharField(max_length=60)
    class_name = models.CharField(max_length=200)
    create_date = models.DateTimeField('create datetime',  auto_now=False,  auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)

    def __str__(self):
        return self.name

class SignalUnit(models.Model):
    descr = models.CharField(max_length=60)
    create_date = models.DateTimeField('create date',auto_now=False, auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)

    def __str__(self):                                       
        return self.descr


class Signal(models.Model):
    unit = models.ForeignKey(SignalUnit, on_delete=models.CASCADE)
    type = models.ForeignKey(SignalType, on_delete=models.CASCADE)
    descr = models.CharField(max_length=300)
    create_date = models.DateTimeField('create date', auto_now=False, auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)

    def __str__(self):                                       
        return self.descr


class DeviceType(models.Model):
    descr = models.CharField(max_length=300)
    create_date = models.DateTimeField('create date', auto_now=False, auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)

    def __str__(self):                                       
        return self.descr

class IOSignalsDeviceType(models.Model):
    IO_TYPE = (
        ('I', 'Input'),
        ('O', 'Output'),
    )
    device = models.ForeignKey(DeviceType, related_name='io_signals', on_delete=models.CASCADE)
    signal = models.ForeignKey(Signal, on_delete=models.CASCADE)
    i_o = models.CharField(max_length=1, choices=IO_TYPE)

class MonitoringDevice(models.Model):
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    descr = models.CharField(max_length=100, null=True, blank=True)
    serial = models.CharField(max_length=40, null=True, blank=True)
    mac_address = models.CharField(max_length=40,null=False, blank=False)
    ip_address = models.CharField(max_length=30,null=True, blank=True)
    create_date = models.DateTimeField('create date', auto_now=False, auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)    
    
    def __str__(self):                                       
        return self.descr

class MeasuredEntity(models.Model):
    MEASURED_ENTITY_TYPE = (
       ('M', 'Machine'),
       ('P', 'Plant'),
    )
    code = models.CharField(max_length=20, null=False, blank=False)
    descr = models.CharField(max_length=200)
    type = models.CharField(max_length=1, choices=MEASURED_ENTITY_TYPE, default='M')
    serial = models.CharField(max_length=60, null=True, blank=True)
    create_date = models.DateTimeField('create datetime', auto_now=False, auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)

    def __str__(self):
        return self.code + ' ' + self.descr

    def __unicode__(self):
        return self.code

class PlantHostSystem(MeasuredEntity):
    id_compania = models.CharField(max_length=60)
    id_sede = models.CharField(max_length=60)
    id_planta = models.CharField(max_length=60)

class MachineHostSystem(MeasuredEntity):
    id_compania = models.CharField(max_length=60)
    id_sede = models.CharField(max_length=60)
    id_planta = models.CharField(max_length=60)
    id_grupo_maquina = models.CharField(max_length=60)
    id_maquina = models.CharField(max_length=60)

class MeasuredEntityBehavior(models.Model):
    measure_entity =  models.ForeignKey(MeasuredEntity, related_name='behaviors', on_delete=models.CASCADE)
    name = models.CharField(max_length=40, null=False, blank=False)
    descr = models.CharField(max_length=160, null=False, blank=False)
    behavior_text = models.TextField(null=True, blank=True)
    create_date = models.DateTimeField('create datetime', auto_now=False, auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)

    def clean(self):
        if len(self.behavior_text) > 0:
            root = Element('program')
            root.text = self.behavior_text
            xml = tostring(root)
            url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
            url = url + defaults.CONTEXT_ROOT + '/'
            url = url + 'checker/behavior'
            r = requests.put(url, data = xml)
            if (r.status_code == 400):
                raise ValidationError("Invalid language request")
            else: 
                tree = ET.ElementTree(ET.fromstring(r.content))
                root = tree.getroot()
                for child in root:
                    lineNumber = child[0].text
                    positionInLine = child[1].text
                    message = child[2].text
                    raise ValidationError("Error in line:" + str(lineNumber) + 
					   " character:" + str(positionInLine) + " " + str(message))
    def __str__(self):
        return self.name  + ' ' + self.descr 
   
class InputOutputPort(models.Model):
    device = models.ForeignKey(MonitoringDevice,related_name='io_ports', on_delete=models.CASCADE)
    port_label = models.CharField(max_length=10, default='COM1',help_text="This field must be included in the mqtt topic")
    signal_type = models.ForeignKey(Signal, on_delete=models.CASCADE)
    measured_entity = models.ForeignKey(MeasuredEntity, related_name='measured_entity', blank= True, null= True, on_delete=models.SET_NULL)
    transformation_text = models.TextField(null=True, blank=True)

    def clean(self):
        if len(self.transformation_text) > 0:
            root = Element('program')
            root.text = self.transformation_text
            xml = tostring(root)
            url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
            url = url + defaults.CONTEXT_ROOT + '/'
            url = url + 'checker/transformation'
            r = requests.put(url, data = xml)
            if (r.status_code == 400):
                raise ValidationError("Invalid language request")
            else: 
                tree = ET.ElementTree(ET.fromstring(r.content))
                root = tree.getroot()
                for child in root:
                    lineNumber = child[0].text
                    positionInLine = child[1].text
                    message = child[2].text
                    raise ValidationError("Error in line:" + str(lineNumber) + 
					   " character:" + str(positionInLine) + " " + str(message))

    def __str__(self):
        return self.port_label

class MeasuredEntityGroup(models.Model):
    descr = models.CharField(max_length=160, null=False, blank=False)
    create_date = models.DateTimeField('create datetime', auto_now=False, auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)

    def __str__(self):
        return self.descr


class IdleReason(models.Model):
    IDLE_CLASSIFICATION = (
       ('A', 'Availability'),
       ('C', 'Capacity'),
       ('P', 'Performance'),
    )

    IDLE_DOWN = (
       ('Y', 'Yes'),
       ('N', 'No'),
    )

    descr = models.CharField(max_length=160, null=False, blank=False)
    group_cd = models.CharField(max_length=60, null=True, blank=True)
    classification = models.CharField(max_length=1, choices=IDLE_CLASSIFICATION, default='A')
    down = models.CharField(max_length=1, choices=IDLE_DOWN, default='Y')
    create_date = models.DateTimeField('create datetime', auto_now=False, auto_now_add=True)
    last_updttm = models.DateTimeField('last datetime', auto_now=True)
    
    def __str__(self):
        return self.descr
    
