from django.test import TestCase
import requests
import json
from canonical.models import Compania


class CompaniaViewTest(TestCase):
    """
       First it deletes all companies with id compania0, which is the one chosen for testing
    """
    def test_view_a_detail_delete(self):
        dict = {'id_compania' : 'compania0', 'descr' : 'compania zero'}
        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/compania/0/'
        response = requests.delete(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 204)

    def test_view_b_post(self):
        dict = {'id_compania' : 'compania0', 'descr' : 'compania zero'}
        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/compania/'
        response = requests.post(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 201)

    def test_view_c_list_get(self):
        url = 'http://localhost:8000/compania/'
        response = requests.get(url, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 200)

    def test_view_d_detail_get(self):
        dict = {'id_compania' : 'compania0', 'descr' : 'compania zero'}
        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/compania/1/'
        response = requests.get(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 200)

    def test_view_e_detail_put(self):
        dict = {'id_compania' : 'compania0', 'descr' : 'compania zero prueba'}
        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/compania/0/'
        response = requests.put(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 200)

class SedeViewTest(TestCase):
    """
       First it deletes all sedes with id (compania0, sede0), which is the one chosen for testing
    """
    def test_view_a_detail_delete(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'descr' : 'Sede 0 compania zero'}
        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/sede/0/'
        response = requests.delete(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 204)

    def test_view_b_post(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'descr' : 'Sede 0 compania zero'}
        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/sede/'
        response = requests.post(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 201)

    def test_view_c_list_get(self):
        url = 'http://localhost:8000/sede/'
        response = requests.get(url, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 200)

    def test_view_d_detail_get(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'descr' : ''}
        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/sede/0/'
        response = requests.get(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 200)

    def test_view_e_detail_put(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'descr' : 'Sede 0 compania zero updated'}
        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/sede/0/'
        response = requests.put(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 200)

class PlantaViewTest(TestCase):
    """
       First it deletes all plantas with id (compania0, sede0, planta0), which is the one chosen for testing
    """
    def test_view_a_detail_delete(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'id_planta' : 'planta0', 'descr' : ''}
        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/planta/0/'
        response = requests.delete(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 204)

    def test_view_b_post(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'id_planta' : 'planta0', 'descr' : 'Planta 0 Sede 0 compania zero', 'last_updttm' : '2017-may-22 00:00:00.000'}
        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/planta/'
        response = requests.post(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 201)

    def test_view_c_list_get(self):
        url = 'http://localhost:8000/planta/'
        response = requests.get(url, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 200)

    def test_view_d_detail_get(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'id_planta' : 'planta0', 'descr' : ''}
        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/planta/0/'
        response = requests.get(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 200)

    def test_view_e_detail_put(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'id_planta' : 'planta0', 'descr' : 'Planta 0 Sede 0 compania zero update'}
        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/planta/0/'
        response = requests.put(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 200)
