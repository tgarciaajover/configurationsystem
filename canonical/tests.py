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

class RazonesParadaViewTest(TestCase):
    """
       First it deletes all razones de parada with id (compania0, sede0, planta0, razonparada0), which is the one chosen for testing
    """
    def test_view_a_detail_delete(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'id_planta' : 'planta0', 
		 'id_razon_parada' : 'razonparada0', 'descr' : '', 'grupo_razon_parada' : '', 
                  'causa_raiz_parada' : '' , 'afecta_capacidad' : '', 
                   'create_date' : '', 'last_updttm' : ''}
        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/razon_parada/0/'
        response = requests.delete(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 204)

    def test_view_b_post(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'id_planta' : 'planta0', 
		 'id_razon_parada' : 'razonparada0', 'descr' : 'razon parada 01', 'grupo_razon_parada' : 'electricidad',
                  'causa_raiz_parada' : 'electricidad' , 'afecta_capacidad' : 'Y', 
                   'create_date' : '2017-may-22 00:00:00.000', 'last_updttm' : '2017-may-22 00:00:00.000'}

        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/razon_parada/'
        response = requests.post(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 201)

    def test_view_c_list_get(self):
        url = 'http://localhost:8000/razon_parada/'
        response = requests.get(url, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 200)

    def test_view_d_detail_get(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'id_planta' : 'planta0', 
		 'id_razon_parada' : 'razonparada0', 'descr' : '', 'grupo_razon_parada' : '', 
                  'causa_raiz_parada' : '' , 'afecta_capacidad' : '','create_date' : '', 'last_updttm' : ''}
        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/razon_parada/0/'
        response = requests.get(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 200)

    def test_view_e_detail_put(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'id_planta' : 'planta0', 
		 'id_razon_parada' : 'razonparada0', 'descr' : 'razon parada 01', 'grupo_razon_parada' : 'electricidad',
                  'causa_raiz_parada' : 'electricidad' , 'afecta_capacidad' : 'Y', 
                   'create_date' : '2017-may-22 00:00:00.000', 'last_updttm' : '2017-may-22 00:00:00.000'}

        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/razon_parada/0/'
        response = requests.put(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 200)

class GrupoMaquinaViewTest(TestCase):
    """
       First it deletes all plantas with id (compania0, sede0, planta0), which is the one chosen for testing
    """
    def test_view_a_detail_delete(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'id_planta' : 'planta0', 
                 'id_grupo_maquina' : 'grupo0', 'descr' : '', 'create_date' : '', 'last_updttm' : ''}

        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/grupo_maquina/0/'
        response = requests.delete(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 204)

    def test_view_b_post(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'id_planta' : 'planta0', 
                 'id_grupo_maquina' : 'grupo0', 'descr' : 'Planta 0 Sede 0 compania 0 grupo 0', 
                  'create_date' : '2017-may-22 00:00:00.000', 'last_updttm' : '2017-may-22 00:00:00.000'}

        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/grupo_maquina/'
        response = requests.post(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 201)

    def test_view_c_list_get(self):
        url = 'http://localhost:8000/grupo_maquina/'
        response = requests.get(url, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 200)

    def test_view_d_detail_get(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'id_planta' : 'planta0', 
                 'id_grupo_maquina' : 'grupo0', 'descr' : '', 
                  'create_date' : '', 'last_updttm' : ''}

        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/grupo_maquina/0/'
        response = requests.get(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 200)

    def test_view_e_detail_put(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'id_planta' : 'planta0', 
                 'id_grupo_maquina' : 'grupo0', 'descr' : 'Planta 0 Sede 0 compania 0 grupo 0 updated', 
                  'create_date' : '2017-may-22 00:00:00.000', 'last_updttm' : '2017-may-22 00:00:00.000'}

        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/grupo_maquina/0/'
        response = requests.put(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 200)

class MaquinaViewTest(TestCase):
    """
       First it deletes all plantas with id (compania0, sede0, planta0), which is the one chosen for testing
    """
    def test_view_a_detail_delete(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'id_planta' : 'planta0', 
                 'id_grupo_maquina' : 'grupo0', 'id_maquina' : 'maquina0', 'descr' : '', 
                  'estado_actual' : '', 'create_date' : '', 'last_updttm' : ''}

        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/maquina/0/'
        response = requests.delete(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 204)

    def test_view_b_post(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'id_planta' : 'planta0', 
                 'id_grupo_maquina' : 'grupo0', 'id_maquina' : 'maquina0', 'descr' : 'Planta 0 Sede 0 compania 0 grupo 0 maquina 0', 
                  'estado_actual' : 'A', 'create_date' : '2017-may-22 00:00:00.000', 'last_updttm' : '2017-may-22 00:00:00.000'}

        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/maquina/'
        response = requests.post(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 201)

    def test_view_c_list_get(self):
        url = 'http://localhost:8000/maquina/'
        response = requests.get(url, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 200)

    def test_view_d_detail_get(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'id_planta' : 'planta0', 
                 'id_grupo_maquina' : 'grupo0', 'id_maquina' : 'maquina0', 'descr' : '', 
                  'estado_actual' : '', 'create_date' : '', 'last_updttm' : ''}

        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/maquina/0/'
        response = requests.get(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 200)

    def test_view_e_detail_put(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'id_planta' : 'planta0', 
                 'id_grupo_maquina' : 'grupo0', 'id_maquina' : 'maquina0', 'descr' : 'Planta 0 Sede 0 compania 0 grupo 0 maquina 0 updated', 
                  'estado_actual' : 'A', 'create_date' : '2017-may-22 00:00:00.000', 'last_updttm' : '2017-may-22 00:00:00.000'}

        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/maquina/0/'
        response = requests.put(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 200)

class PlanProductionViewTest(TestCase):
    """
       First it deletes all plantas with id (compania0, sede0, planta0), which is the one chosen for testing
    """
    def test_view_a_detail_delete(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'id_planta' : 'planta0', 
                 'id_grupo_maquina' : 'grupo0', 'id_maquina' : 'maquina0', 'ano' : '2017',
                   'mes' : '5', 'create_date' : '', 'last_updttm' : ''}

        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/plan_produccion/0/'
        response = requests.delete(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 204)

    def test_view_b_post(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'id_planta' : 'planta0', 
                 'id_grupo_maquina' : 'grupo0', 'id_maquina' : 'maquina0', 'ano' : '2017',
                   'mes' : '5', 'create_date' : '2017-may-22 00:00:00.000', 'last_updttm' : '2017-may-22 00:00:00.000'}

        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/plan_produccion/'
        response = requests.post(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 201)

    def test_view_c_list_get(self):
        url = 'http://localhost:8000/plan_produccion/'
        response = requests.get(url, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 200)

    def test_view_d_detail_get(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'id_planta' : 'planta0', 
                 'id_grupo_maquina' : 'grupo0', 'id_maquina' : 'maquina0', 'ano' : '2017',
                   'mes' : '5', 'create_date' : '', 'last_updttm' : ''}

        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/plan_produccion/0/'
        response = requests.get(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 200)

    def test_view_e_detail_put(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'id_planta' : 'planta0', 
                 'id_grupo_maquina' : 'grupo0', 'id_maquina' : 'maquina0', 'ano' : '2017',
                   'mes' : '5', 'create_date' : '2017-may-22 00:00:00.000', 'last_updttm' : '2017-may-22 00:00:00.000'}

        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/plan_produccion/0/'
        response = requests.put(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 200)

class OrdenProduccionPlaneadaViewTest(TestCase):
    """
       First it deletes all orden produccion planeada with id (compania0, sede0, planta0), which is the one chosen for testing
    """
    def test_view_a_detail_delete(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'id_planta' : 'planta0', 
                 'id_grupo_maquina' : 'grupo0', 'id_maquina' : 'maquina0', 'ano' : '2017',
                   'mes' : '5', 'id_produccion' : 'prod01', 'id_articulo' : '',
                   'descr_articulo' : '', 'fechahora_inicial' : '',
                   'fechahora_final': '', 'num_horas' : '0',
                   'cantidad_producir' : '0', 'tasa_esperada' : '0', 'velocidad_esperada' : '0.0',
                   'create_date' : '', 'last_updttm' : ''}

        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/orden_produccion_planeada/0/'
        response = requests.delete(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 204)

    def test_view_b_post(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'id_planta' : 'planta0', 
                 'id_grupo_maquina' : 'grupo0', 'id_maquina' : 'maquina0', 'ano' : '2017',
                   'mes' : '5', 'id_produccion' : 'prod01', 'id_articulo' : 'art01',
                   'descr_articulo' : 'articulo prueba', 'fechahora_inicial' : '2017-May-22 12:00:00.000',
                   'fechahora_final': '2017-may-22 14:00:00.000', 'num_horas' : '2',
                   'cantidad_producir' : '40', 'tasa_esperada' : '1', 'velocidad_esperada' : '1.0',
                   'create_date' : '2017-may-22 00:00:00.000', 'last_updttm' : '2017-May-22 00:00:00.000'}

        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/orden_produccion_planeada/'
        response = requests.post(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 201)

    def test_view_c_list_get(self):
        url = 'http://localhost:8000/orden_produccion_planeada/'
        response = requests.get(url, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 200)

    def test_view_d_detail_get(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'id_planta' : 'planta0', 
                 'id_grupo_maquina' : 'grupo0', 'id_maquina' : 'maquina0', 'ano' : '2017',
                   'mes' : '5', 'id_produccion' : 'prod01', 'id_articulo' : '',
                   'descr_articulo' : '', 'fechahora_inicial' : '',
                   'fechahora_final': '', 'num_horas' : '0',
                   'cantidad_producir' : '0', 'tasa_esperada' : '0', 'velocidad_esperada' : '0.0',
                   'create_date' : '', 'last_updttm' : ''}

        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/orden_produccion_planeada/0/'
        response = requests.get(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 200)

    def test_view_e_detail_put(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'id_planta' : 'planta0', 
                 'id_grupo_maquina' : 'grupo0', 'id_maquina' : 'maquina0', 'ano' : '2017',
                   'mes' : '5', 'id_produccion' : 'prod01', 'id_articulo' : 'art01',
                   'descr_articulo' : 'articulo prueba', 'fechahora_inicial' : '2017-may-22 12:00:00.000',
                   'fechahora_final': '2017-may-22 14:00:00.000', 'num_horas' : '2',
                   'cantidad_producir' : '40', 'tasa_esperada' : '1', 'velocidad_esperada' : '1.0',
                   'create_date' : '2017-may-22 00:00:00.000', 'last_updttm' : '2017-may-22 00:00:00.000'}

        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/orden_produccion_planeada/0/'
        response = requests.put(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 200)

class ParadaPlaneadaViewTest(TestCase):
    """
       First it deletes all orden produccion planeada with id (compania0, sede0, planta0), which is the one chosen for testing
    """
    def test_view_a_detail_delete(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'id_planta' : 'planta0', 
                 'id_grupo_maquina' : 'grupo0', 'id_maquina' : 'maquina0', 'ano' : '2017',
                   'mes' : '5', 'id_produccion' : 'prod01', 'fechahora_inicial' : '',
                   'fechahora_final': '', 'create_date' : '', 'last_updttm' : ''}

        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/parada_planeada/0/'
        response = requests.delete(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 204)

    def test_view_b_post(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'id_planta' : 'planta0', 
                 'id_grupo_maquina' : 'grupo0', 'id_maquina' : 'maquina0', 'ano' : '2017',
                   'mes' : '5', 'id_produccion' : 'prod01', 'fechahora_inicial' : '2017-May-22 12:00:00.000',
                   'fechahora_final': '2017-may-22 14:00:00.000', 
                   'create_date' : '2017-may-22 00:00:00.000', 'last_updttm' : '2017-May-22 00:00:00.000'}

        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/parada_planeada/'
        response = requests.post(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 201)

    def test_view_c_list_get(self):
        url = 'http://localhost:8000/parada_planeada/'
        response = requests.get(url, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 200)

    def test_view_d_detail_get(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'id_planta' : 'planta0', 
                 'id_grupo_maquina' : 'grupo0', 'id_maquina' : 'maquina0', 'ano' : '2017',
                   'mes' : '5', 'id_produccion' : 'prod01', 'fechahora_inicial' : '',
                   'fechahora_final': '', 'create_date' : '', 'last_updttm' : ''}

        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/parada_planeada/0/'
        response = requests.get(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 200)

    def test_view_e_detail_put(self):
        dict = {'id_compania' : 'compania0', 'id_sede' : 'sede0', 'id_planta' : 'planta0', 
                 'id_grupo_maquina' : 'grupo0', 'id_maquina' : 'maquina0', 'ano' : '2017',
                   'mes' : '5', 'id_produccion' : 'prod01', 'fechahora_inicial' : '2017-may-22 12:00:00.000',
                   'fechahora_final': '2017-may-22 14:00:00.000', 'create_date' : '2017-may-22 00:00:00.000', 
                    'last_updttm' : '2017-may-22 00:00:00.000'}

        jsonText = json.dumps(dict)
        url = 'http://localhost:8000/parada_planeada/0/'
        response = requests.put(url, data = jsonText, auth=('iotajover', 'iotajover'))
        self.assertEqual(response.status_code, 200)
