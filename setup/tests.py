from django.test import TestCase
import requests
import json
import datetime
from datetime import timedelta
import setup.defaults as defaults

from setup.models import SignalUnit
from setup.models import SignalType
from setup.models import Signal
from setup.models import DeviceType
from setup.models import MonitoringDevice
from setup.models import MeasuredEntityBehavior
from setup.models import MeasuredEntity
from setup.models import PlantHostSystem
from setup.models import MeasuredEntityScheduledEvent
from setup.models import MeasuredEntityStateBehavior
from setup.models import MeasuredEntityTransitionState

from setup.serializers import SignalUnitSerializer
from setup.serializers import SignalTypeSerializer
from setup.serializers import SignalSerializer
from setup.serializers import DeviceTypeSerializer
from setup.serializers import MonitoringDeviceSerializer
from setup.serializers import MeasuredEntityBehaviorSerializer
from setup.serializers import MeasuredEntitySerializer
from setup.serializers import PlantHostSystemSerializer
from setup.serializers import MeasuredEntityScheduledEventSerializer
from setup.serializers import MeasuredEntityStateBehaviorSerializer
from setup.serializers import MeasuredEntityTransitionStateSerializer

from rest_framework.renderers import JSONRenderer


# Create your tests here.

class SignalUnitInterfaceTest(TestCase):

    def test_put(self):
        signalUnit = SignalUnit.objects.get(id=1)
        serializer = SignalUnitSerializer(signalUnit)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'SignalUnit' + '/' + str(signalUnit.id)
        response = requests.put(url, data = content)
        self.assertEqual(response.status_code, 204)
        
    def test_get(self):
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'SignalUnit' + '/' + str(1)
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        print(response.text)

    def test_delete(self):
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'SignalUnit' + '/' + str(1)
        response = requests.delete(url)
        self.assertEqual(response.status_code, 204)

class SignalTypeInterfaceTest(TestCase):

    def test_put(self):
        signalType = SignalType.objects.get(id=5)
        serializer = SignalTypeSerializer(signalType)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'SignalType' + '/' + str(signalType.id)
        response = requests.put(url, data = content)
        self.assertEqual(response.status_code, 204)
        
    def test_get(self):
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'SignalType' + '/' + str(5)
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        print(response.text)

    def test_delete(self):
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'SignalType' + '/' + str(5)
        response = requests.delete(url)
        self.assertEqual(response.status_code, 204)

class SignalInterfaceTest(TestCase):

    def test_put(self):
        signal = Signal.objects.get(id=5)
        serializer = SignalSerializer(signal)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'Signal' + '/' + str(signal.id)
        response = requests.put(url, data = content)
        self.assertEqual(response.status_code, 204)
        
    def test_get(self):
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'Signal' + '/' + str(5)
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        print(response.text)

    def test_delete(self):
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'Signal' + '/' + str(5)
        response = requests.delete(url)
        self.assertEqual(response.status_code, 204)

class DeviceTypeInterfaceTest(TestCase):

    def test_put(self):
        deviceType = DeviceType.objects.get(id=1)
        serializer = DeviceTypeSerializer(deviceType)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'DeviceType' + '/' + str(deviceType.id)
        response = requests.put(url, data = content)
        self.assertEqual(response.status_code, 204)
        
    def test_get(self):
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'DeviceType' + '/' + str(14)
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        print(response.text)

    def test_delete(self):
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'DeviceType' + '/' + str(1)
        response = requests.delete(url)
        self.assertEqual(response.status_code, 204)

class MonitoringDeviceInterfaceTest(TestCase):

    def test_put(self):
        obj = MonitoringDevice.objects.get(id=5)
        serializer = MonitoringDeviceSerializer(obj)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MonitoringDevice' + '/' + str(obj.id)
        response = requests.put(url, data = content)
        self.assertEqual(response.status_code, 204)
        
    def test_get(self):
        obj = MonitoringDevice.objects.get(id=5)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MonitoringDevice' + '/' + str(obj.id)
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        print(response.text)

    def test_delete(self):
        obj = MonitoringDevice.objects.get(id=5)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MonitoringDevice' + '/' + str(obj.id)
        response = requests.delete(url)
        self.assertEqual(response.status_code, 204)


class MeasuredEntityBehaviorInterfaceTest(TestCase):

    def test_put(self):
        obj = MeasuredEntityBehavior.objects.get(id=14)
        serializer = MeasuredEntityBehaviorSerializer(obj)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MeasuredEntity' + '/' + str(obj.measure_entity_id) + '/Behavior/' + str(obj.id) 
        response = requests.put(url, data = content)
        self.assertEqual(response.status_code, 204)
        
    def test_get(self):
        obj = MeasuredEntityBehavior.objects.get(id=14)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MeasuredEntity' + '/' + str(obj.measure_entity_id) + '/Behavior/' + str(obj.id) 
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        print(response.text)

    def test_delete(self):
        obj = MeasuredEntityBehavior.objects.get(id=14)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MeasuredEntity' + '/' + str(obj.measure_entity_id) + '/Behavior/' + str(obj.id) 
        response = requests.delete(url)
        self.assertEqual(response.status_code, 204)

class PlantHostSystemInterfaceTest(TestCase):

    def test_put(self):
        obj = PlantHostSystem.objects.get(id=99)
        serializer = PlantHostSystemSerializer(obj)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MeasuredEntity' + '/' + str(obj.id) 
        response = requests.put(url, data = content)
        self.assertEqual(response.status_code, 204)
        
    def test_get(self):
        obj = PlantHostSystem.objects.get(id=99)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MeasuredEntity' + '/' + str(obj.id)
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        print(response.text)

    def test_delete(self):
        obj = PlantHostSystem.objects.get(id=99)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MeasuredEntity' + '/' + str(obj.id)
        response = requests.delete(url)
        self.assertEqual(response.status_code, 204)

class MeasuredEntityStateBehaviorInterfaceTest(TestCase):
    def test_put(self):
        obj = MeasuredEntityStateBehavior.objects.get(id=3)
        serializer = MeasuredEntityStateBehaviorSerializer(obj)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MeasuredEntity' + '/' + str(obj.measure_entity_id) + '/StateBehavior/' + str(obj.id) 
        response = requests.put(url, data = content)
        self.assertEqual(response.status_code, 204)
        
    def test_get(self):
        obj = MeasuredEntityStateBehavior.objects.get(id=3)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MeasuredEntity' + '/' + str(obj.measure_entity_id) + '/StateBehavior/' + str(obj.id) 
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        print(response.text)

    def test_delete(self):
        obj = MeasuredEntityStateBehavior.objects.get(id=3)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MeasuredEntity' + '/' + str(obj.measure_entity_id) + '/StateBehavior/' + str(obj.id) 
        response = requests.delete(url)
        self.assertEqual(response.status_code, 204)


class MeasuredEntityScheduledEventInterfaceTest(TestCase):
    def test_put(self):
        obj = MeasuredEntityScheduledEvent.objects.get(id=3)
        serializer = MeasuredEntityScheduledEventSerializer(obj)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MeasuredEntity' + '/' + str(obj.measure_entity_id) + '/ScheduledEvent/' + str(obj.id)  
        response = requests.put(url, data = content)
        self.assertEqual(response.status_code, 204)
        
    def test_get(self):
        obj = MeasuredEntityScheduledEvent.objects.get(id=3)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MeasuredEntity' + '/' + str(obj.measure_entity_id) + '/ScheduledEvent/' + str(obj.id)  
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        print(response.text)

    def test_delete(self):
        obj = MeasuredEntityScheduledEvent.objects.get(id=3)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MeasuredEntity' + '/' + str(obj.measure_entity_id) + '/ScheduledEvent/' + str(obj.id)  
        response = requests.delete(url)
        self.assertEqual(response.status_code, 204)

class MeasuredEntityTransitionStateInterfaceTest(TestCase):
    def test_put(self):
        obj = MeasuredEntityTransitionState.objects.get(id=4)
        serializer = MeasuredEntityTransitionStateSerializer(obj)
        content = JSONRenderer().render(serializer.data)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MeasuredEntity' + '/' + str(obj.measure_entity_id) + '/StateTransition/' + str(obj.id)  
        response = requests.put(url, data = content)
        self.assertEqual(response.status_code, 204)
        
    def test_get(self):
        obj = MeasuredEntityTransitionState.objects.get(id=4)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MeasuredEntity' + '/' + str(obj.measure_entity_id) + '/StateTransition/' + str(obj.id)  
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        print(response.text)

    def test_delete(self):
        obj = MeasuredEntityTransitionState.objects.get(id=4)
        url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
        url = url + defaults.CONTEXT_ROOT + '/'
        url = url + 'MeasuredEntity' + '/' + str(obj.measure_entity_id) + '/StateTransition/' + str(obj.id)  
        response = requests.delete(url)
        self.assertEqual(response.status_code, 204)
