from django.test import TestCase
import requests
import json
from canonical.models import Compania
import datetime
from datetime import timedelta

host = 'http://192.168.0.171'
port = ':8000'
url_prefix = '/'


class CompaniaViewTest(TestCase):
    """
       First it deletes all companies with id compania0, which is the one chosen for testing
    """

    def test_view_a_detail_delete(self, token=None):
        dict = {'id_compania': 'compania0', 'descr': 'compania zero'}
        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'compania/0/'
        print(token)
        if not token:
            response = requests.delete(url, data=jsonText,
                                       auth=('admin', 'admin2018'))
        else:
            response = requests.delete(url, data=jsonText,
                                       headers=token)
        self.assertEqual(response.status_code, 204)

    def test_view_b_post(self, token=None):
        dict = {'id_compania': 'compania0', 'descr': 'compania zero'}
        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'compania/'
        if not token:
            response = requests.post(url, data=jsonText,
                                     auth=('admin', 'admin2018'))
        else:
            response = requests.post(url, data=jsonText,
                                     headers=token)
        self.assertEqual(response.status_code, 201)

    def test_view_c_list_get(self, token=None):
        url = host + port + url_prefix + 'compania/'
        if not token:
            response = requests.get(url, auth=('admin', 'admin'))
        else:
            response = requests.get(url, headers=token)
        self.assertEqual(response.status_code, 200)

    def test_view_d_detail_get(self, token=None):
        dict = {'id_compania': 'compania0', 'descr': 'compania zero'}
        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'compania/1/'
        if not token:
            response = requests.get(url, data=jsonText,
                                    auth=('admin', 'admin2018'))
        else:
            response = requests.get(url, data=jsonText,
                                    headers=token)
        self.assertEqual(response.status_code, 200)

    def test_view_e_detail_put(self, token=None):
        dict = {'id_compania': 'compania0', 'descr': 'compania zero prueba'}
        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'compania/0/'
        if not token:
            response = requests.put(url, data=jsonText,
                                    auth=('admin', 'admin2018'))
        else:
            response = requests.put(url, data=jsonText,
                                    headers=token)
        self.assertEqual(response.status_code, 200)


class SedeViewTest(TestCase):
    """
       First it deletes all sedes with id (compania0, sede0), which is the one chosen for testing
    """

    def test_view_a_detail_delete(self, token=None):
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0',
                'descr': 'Sede 0 compania zero'}
        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'sede/0/'
        if not token:
            response = requests.delete(url, data=jsonText,
                                       auth=('admin', 'admin2018'))
        else:
            response = requests.delete(url, data=jsonText,
                                       headers=token)
        self.assertEqual(response.status_code, 204)

    def test_view_b_post(self, token=None):
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0',
                'descr': 'Sede 0 compania zero'}
        jsonText = json.dumps(dict)
        url = url = host + port + url_prefix + 'sede/'
        if not token:
            response = requests.post(url, data=jsonText,
                                     auth=('admin', 'admin2018'))
        else:
            response = requests.post(url, data=jsonText,
                                     headers=token)
        self.assertEqual(response.status_code, 201)

    def test_view_c_list_get(self, token=None):
        url = host + port + url_prefix + 'sede/'
        if not token:
            response = requests.get(url, auth=('admin', 'admin'))
        else:
            response = requests.get(url, headers=token)
        self.assertEqual(response.status_code, 200)

    def test_view_d_detail_get(self, token=None):
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0', 'descr': ''}
        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'sede/0/'
        if not token:
            response = requests.get(url, data=jsonText,
                                    auth=('admin', 'admin2018'))
        else:
            response = requests.get(url, data=jsonText,
                                    headers=token)
        self.assertEqual(response.status_code, 200)

    def test_view_e_detail_put(self, token=None):
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0',
                'descr': 'Sede 0 compania zero updated'}
        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'sede/0/'
        if not token:
            response = requests.put(url, data=jsonText,
                                    auth=('admin', 'admin2018'))
        else:
            response = requests.put(url, data=jsonText,
                                    headers=token)
        self.assertEqual(response.status_code, 200)


class PlantaViewTest(TestCase):
    """
       First it deletes all plantas with id (compania0, sede0, planta0), which is the one chosen for testing
    """

    def test_view_a_detail_delete(self, token=None):
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0',
                'id_planta': 'planta0', 'descr': ''}
        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'planta/0/'
        if not token:
            response = requests.delete(url, data=jsonText,
                                       auth=('admin', 'admin2018'))
        else:
            response = requests.delete(url, data=jsonText,
                                       headers=token)
        self.assertEqual(response.status_code, 204)

    def test_view_b_post(self, token=None):
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0',
                'id_planta': 'planta0',
                'descr': 'Planta 0 Sede 0 compania zero',
                'last_updttm': '2017-05-22 00:00:00.000'}
        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'planta/'
        if not token:
            response = requests.post(url, data=jsonText,
                                     auth=('admin', 'admin2018'))
        else:
            response = requests.post(url, data=jsonText,
                                     headers=token)
        self.assertEqual(response.status_code, 201)

    def test_view_c_list_get(self, token=None):
        url = host + port + url_prefix + 'planta/'
        if not token:
            response = requests.get(url, auth=('admin', 'admin'))
        else:
            response = requests.get(url, headers=token)
        self.assertEqual(response.status_code, 200)

    def test_view_d_detail_get(self, token=None):
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0',
                'id_planta': 'planta0', 'descr': ''}
        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'planta/0/'
        if not token:
            response = requests.get(url, data=jsonText,
                                    auth=('admin', 'admin2018'))
        else:
            response = requests.get(url, data=jsonText,
                                    headers=token)
        self.assertEqual(response.status_code, 200)

    def test_view_e_detail_put(self, token=None):
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0',
                'id_planta': 'planta0',
                'descr': 'Planta 0 Sede 0 compania zero update'}
        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'planta/0/'
        if not token:
            response = requests.put(url, data=jsonText,
                                    auth=('admin', 'admin2018'))
        else:
            response = requests.put(url, data=jsonText,
                                    headers=token)
        self.assertEqual(response.status_code, 200)


class RazonesParadaViewTest(TestCase):
    """
       First it deletes all razones de parada with id (compania0, sede0, planta0, razonparada0), which is the one chosen for testing
    """

    def test_view_a_detail_delete(self, token=None):
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0',
                'id_planta': 'planta0',
                'id_razon_parada': 'razonparada0', 'descr': '',
                'grupo_razon_parada': '',
                'causa_raiz_parada': '', 'afecta_capacidad': '',
                'clasificacion': '',
                'create_date': '', 'last_updttm': ''}
        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'razon_parada/0/'
        if not token:
            response = requests.delete(url, data=jsonText,
                                       auth=('admin', 'admin2018'))
        else:
            response = requests.delete(url, data=jsonText,
                                       headers=token)
        self.assertEqual(response.status_code, 204)

    def test_view_b_post(self, token=None):
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0',
                'id_planta': 'planta0',
                'id_razon_parada': 'razonparada0', 'descr': 'razon parada 01',
                'grupo_razon_parada': 'electricidad',
                'causa_raiz_parada': 'electricidad', 'afecta_capacidad': 'Y',
                'clasificacion': 'A',
                'create_date': '2017-05-22 00:00:00.000',
                'last_updttm': '2017-05-22 00:00:00.000'}

        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'razon_parada/'
        if not token:
            response = requests.post(url, data=jsonText,
                                     auth=('admin', 'admin2018'))
        else:
            response = requests.post(url, data=jsonText,
                                     headers=token)
        self.assertEqual(response.status_code, 201)

    def test_view_c_list_get(self, token=None):
        url = host + port + url_prefix + 'razon_parada/'
        if not token:
            response = requests.get(url, auth=('admin', 'admin'))
        else:
            response = requests.get(url, auth=('admin', 'admin'),
                                    headers=token)
        self.assertEqual(response.status_code, 200)

    def test_view_d_detail_get(self, token=None):
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0',
                'id_planta': 'planta0',
                'id_razon_parada': 'razonparada0', 'descr': '',
                'grupo_razon_parada': '',
                'causa_raiz_parada': '', 'afecta_capacidad': '',
                'clasificacion': '', 'create_date': '', 'last_updttm': ''}
        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'razon_parada/0/'
        if not token:
            response = requests.get(url, data=jsonText,
                                    auth=('admin', 'admin2018'))
        else:
            response = requests.get(url, data=jsonText,
                                    headers=token)
        self.assertEqual(response.status_code, 200)

    def test_view_e_detail_put(self, token=None):
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0',
                'id_planta': 'planta0',
                'id_razon_parada': 'razonparada0', 'descr': 'razon parada 01',
                'grupo_razon_parada': 'electricidad',
                'causa_raiz_parada': 'electricidad', 'afecta_capacidad': 'Y',
                'clasificacion': 'A',
                'create_date': '2017-05-22 00:00:00.000',
                'last_updttm': '2017-05-22 00:00:00.000'}

        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'razon_parada/0/'
        if not token:
            response = requests.put(url, data=jsonText,
                                    auth=('admin', 'admin2018'))
        else:
            response = requests.put(url, data=jsonText,
                                    headers=token)
        self.assertEqual(response.status_code, 200)


class GrupoMaquinaViewTest(TestCase):
    """
       First it deletes all plantas with id (compania0, sede0, planta0), which is the one chosen for testing
    """

    def test_view_a_detail_delete(self, token=None):
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0',
                'id_planta': 'planta0',
                'id_grupo_maquina': 'grúpo0', 'descr': '', 'create_date': '',
                'last_updttm': ''}

        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'grupo_maquina/0/'
        if not token:
            response = requests.delete(url, data=jsonText,
                                       auth=('admin', 'admin2018'))
        else:
            response = requests.delete(url, data=jsonText,
                                       headers=token)
        self.assertEqual(response.status_code, 204)

    def test_view_b_post(self, token=None):
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0',
                'id_planta': 'planta0',
                'id_grupo_maquina': 'grupo0',
                'descr': 'Plánta 0 Sede 0 compania 0 grupo 0',
                'create_date': '2017-05-22 00:00:00.000',
                'last_updttm': '2017-05-22 00:00:00.000'}

        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'grupo_maquina/'
        if not token:
            response = requests.post(url, data=jsonText,
                                     auth=('admin', 'admin2018'))
        else:
            response = requests.post(url, data=jsonText,
                                     headers=token)
        self.assertEqual(response.status_code, 201)

    def test_view_c_list_get(self, token=None):
        url = host + port + url_prefix + 'grupo_maquina/'
        if not token:
            response = requests.get(url, auth=('admin', 'admin'))
        else:
            response = requests.get(url, headers=token)
        self.assertEqual(response.status_code, 200)

    def test_view_d_detail_get(self, token=None):
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0',
                'id_planta': 'planta0',
                'id_grupo_maquina': 'grupo0', 'descr': '',
                'create_date': '', 'last_updttm': ''}

        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'grupo_maquina/0/'
        if not token:
            response = requests.get(url, data=jsonText,
                                    auth=('admin', 'admin2018'))
        else:
            response = requests.get(url, data=jsonText,
                                    headers=token)
        self.assertEqual(response.status_code, 200)

    def test_view_e_detail_put(self, token=None):
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0',
                'id_planta': 'planta0',
                'id_grupo_maquina': 'grupo0',
                'descr': 'Planta 0 Sede 0 compania 0 grupo 0 updated',
                'create_date': '2017-05-22 00:00:00.000',
                'last_updttm': '2017-05-22 00:00:00.000'}

        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'grupo_maquina/0/'
        if not token:
            response = requests.put(url, data=jsonText,
                                    auth=('admin', 'admin2018'))
        else:
            response = requests.put(url, data=jsonText,
                                    headers=token)
        self.assertEqual(response.status_code, 200)


class MaquinaViewTest(TestCase):
    """
       First it deletes all plantas with id (compania0, sede0, planta0), which is the one chosen for testing
    """

    def test_view_a_detail_delete(self, token=None):
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0',
                'id_planta': 'planta0',
                'id_grupo_maquina': 'grupo0', 'id_maquina': 'maquina0',
                'descr': '',
                'estado_actual': '', 'create_date': '', 'last_updttm': ''}

        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'maquina/0/'
        if not token:
            response = requests.delete(url, data=jsonText,
                                       auth=('admin', 'admin2018'))
        else:
            response = requests.delete(url, data=jsonText,
                                       headers=token)
        self.assertEqual(response.status_code, 204)

    def test_view_b_post(self, token=None):
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0',
                'id_planta': 'planta0',
                'id_grupo_maquina': 'grupo0', 'id_maquina': 'maquina0',
                'descr': 'Planta 0 Sede 0 compania 0 grupo 0 maquina 0',
                'estado_actual': 'A', 'create_date': '2017-05-22 00:00:00.000',
                'last_updttm': '2017-05-22 00:00:00.000'}

        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'maquina/'
        if not token:
            response = requests.post(url, data=jsonText,
                                     auth=('admin', 'admin2018'))
        else:
            response = requests.post(url, data=jsonText,
                                     headers=token)
        self.assertEqual(response.status_code, 201)

    def test_view_c_list_get(self, token=None):
        url = host + port + url_prefix + 'maquina/'
        if not token:
            response = requests.get(url, auth=('admin', 'admin'))
        else:
            response = requests.get(url, headers=token)
        self.assertEqual(response.status_code, 200)

    def test_view_d_detail_get(self, token=None):
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0',
                'id_planta': 'planta0',
                'id_grupo_maquina': 'grupo0', 'id_maquina': 'maquina0',
                'descr': '',
                'estado_actual': '', 'create_date': '', 'last_updttm': ''}

        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'maquina/0/'
        if not token:
            response = requests.get(url, data=jsonText,
                                    auth=('admin', 'admin2018'))
        else:
            response = requests.get(url, data=jsonText,
                                    headers=token)

        self.assertEqual(response.status_code, 200)

    def test_view_e_detail_put(self, token=None):
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0',
                'id_planta': 'planta0',
                'id_grupo_maquina': 'grupo0', 'id_maquina': 'maquina0',
                'descr': 'Planta 0 Sede 0 compania 0 grupo 0 maquina 0 updated',
                'estado_actual': 'A', 'create_date': '2017-05-22 00:00:00.000',
                'last_updttm': '2017-05-22 00:00:00.000'}

        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'maquina/0/'
        if not token:
            response = requests.put(url, data=jsonText,
                                    auth=('admin', 'admin2018'))
        else:
            response = requests.put(url, data=jsonText,
                                    headers=token)
        self.assertEqual(response.status_code, 200)


class PlanProductionViewTest(TestCase):
    """
       First it deletes all plantas with id (compania0, sede0, planta0), which is the one chosen for testing
    """

    def test_view_a_detail_delete(self, token=None):
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0',
                'id_planta': 'planta0',
                'id_grupo_maquina': 'grupo0', 'id_maquina': 'maquina0',
                'ano': '2017',
                'mes': '7', 'create_date': '', 'last_updttm': ''}

        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'plan_produccion/0/'
        if not token:
            response = requests.delete(url, data=jsonText,
                                       auth=('admin', 'admin2018'))
        else:
            response = requests.delete(url, data=jsonText,
                                       headers=token)
        self.assertEqual(response.status_code, 204)

    def test_view_b_post(self, token=None):
        currrentdatetime = datetime.datetime.now()
        datetimeStr = currrentdatetime.strftime("%Y-%m-%d %H:%M:%S.%f")
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0',
                'id_planta': 'planta0',
                'id_grupo_maquina': 'grupo0', 'id_maquina': 'maquina0',
                'ano': '2017',
                'mes': '7', 'create_date': datetimeStr,
                'last_updttm': datetimeStr}

        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'plan_produccion/'
        if not token:
            response = requests.post(url, data=jsonText,
                                     auth=('admin', 'admin2018'))
        else:
            response = requests.post(url, data=jsonText,
                                     headers=token)
        self.assertEqual(response.status_code, 201)

    def test_view_c_list_get(self, token=None):
        url = host + port + url_prefix + 'plan_produccion/'
        if not token:
            response = requests.get(url, auth=('admin', 'admin'))
        else:
            response = requests.get(url, headers=token)
        self.assertEqual(response.status_code, 200)

    def test_view_d_detail_get(self, token=None):
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0',
                'id_planta': 'planta0',
                'id_grupo_maquina': 'grupo0', 'id_maquina': 'maquina0',
                'ano': '2017',
                'mes': '5', 'create_date': '', 'last_updttm': ''}

        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'plan_produccion/0/'
        if not token:
            response = requests.get(url, data=jsonText,
                                    auth=('admin', 'admin2018'))
        else:
            response = requests.get(url, data=jsonText,
                                    headers=token)
        self.assertEqual(response.status_code, 200)

    def test_view_e_detail_put(self, token=None):
        currrentdatetime = datetime.datetime.now()
        datetimeStr = currrentdatetime.strftime("%Y-%m-%d %H:%M:%S.%f")
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0',
                'id_planta': 'planta0',
                'id_grupo_maquina': 'grupo0', 'id_maquina': 'maquina0',
                'ano': '2017',
                'mes': '5', 'create_date': datetimeStr,
                'last_updttm': datetimeStr}

        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'plan_produccion/0/'
        if not token:
            response = requests.put(url, data=jsonText,
                                    auth=('admin', 'admin2018'))
        else:
            response = requests.put(url, data=jsonText,
                                    headers=token)
        self.assertEqual(response.status_code, 200)


class OrdenProduccionPlaneadaViewTest(TestCase):
    """
       First it deletes all orden produccion planeada with id (compania0, sede0, planta0), which is the one chosen for testing
    """

    def test_view_a_detail_delete(self, token=None):
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0',
                'id_planta': 'planta0',
                'id_grupo_maquina': 'grupo0', 'id_maquina': 'maquina0',
                'ano': '2017',
                'mes': '7', 'id_produccion': 'prod02', 'id_articulo': '',
                'descr_articulo': '', 'fechahora_inicial': '',
                'fechahora_final': '', 'num_horas': '0',
                'cantidad_producir': '0', 'tasa_esperada': '0',
                'velocidad_esperada': '0.0',
                'create_date': '', 'last_updttm': ''}

        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'orden_produccion_planeada/0/'
        if not token:
            response = requests.delete(url, data=jsonText,
                                       auth=('admin', 'admin2018'))
        else:
            response = requests.delete(url, data=jsonText,
                                       headers=token)
        self.assertEqual(response.status_code, 204)

    def test_view_b_post(self, token=None):
        currrentdatetime = datetime.datetime.now()
        datetimeStr = currrentdatetime.strftime("%Y-%m-%d %H:%M:%S.%f")
        d = timedelta(days=2)
        todatetime = currrentdatetime + d
        fromDateTimeStr = currrentdatetime.strftime("%Y-%m-%d %H:%M:%S.%f")
        toDateTimeStr = todatetime.strftime("%Y-%m-%d %H:%M:%S.%f")
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0',
                'id_planta': 'planta0',
                'id_grupo_maquina': 'grupo0', 'id_maquina': 'maquina0',
                'ano': '2017',
                'mes': '7', 'id_produccion': 'prod02', 'id_articulo': 'art02',
                'descr_articulo': 'articulo prueba 2',
                'fechahora_inicial': fromDateTimeStr,
                'fechahora_final': toDateTimeStr, 'num_horas': '48',
                'cantidad_producir': '100', 'tasa_esperada': '1.56',
                'velocidad_esperada': '1.35',
                'create_date': datetimeStr, 'last_updttm': datetimeStr}

        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'orden_produccion_planeada/'
        if not token:
            response = requests.post(url, data=jsonText,
                                     auth=('admin', 'admin2018'))
        else:
            response = requests.post(url, data=jsonText,
                                     headers=token)
        self.assertEqual(response.status_code, 201)

    def test_view_c_list_get(self, token=None):
        url = host + port + url_prefix + 'orden_produccion_planeada/'
        if not token:
            response = requests.get(url, auth=('admin', 'admin'))
        else:
            response = requests.get(url, auth=('admin', 'admin'), headers=token)
        self.assertEqual(response.status_code, 200)

    def test_view_d_detail_get(self, token=None):
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0',
                'id_planta': 'planta0',
                'id_grupo_maquina': 'grupo0', 'id_maquina': 'maquina0',
                'ano': '2017',
                'mes': '5', 'id_produccion': 'prod01', 'id_articulo': '',
                'descr_articulo': '', 'fechahora_inicial': '',
                'fechahora_final': '', 'num_horas': '0',
                'cantidad_producir': '0', 'tasa_esperada': '0',
                'velocidad_esperada': '0.0',
                'create_date': '', 'last_updttm': ''}

        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'orden_produccion_planeada/0/'
        if not token:
            response = requests.get(url, data=jsonText,
                                    auth=('admin', 'admin2018'))
        else:
            response = requests.get(url, data=jsonText,
                                    headers=token)
        self.assertEqual(response.status_code, 200)

    def test_view_e_detail_put(self, token=None):
        currrentdatetime = datetime.datetime.now()
        datetimeStr = currrentdatetime.strftime("%Y-%m-%d %H:%M:%S.%f")
        d = timedelta(days=2)
        todatetime = currrentdatetime + d
        fromDateTimeStr = currrentdatetime.strftime("%Y-%m-%d %H:%M:%S.%f")
        toDateTimeStr = todatetime.strftime("%Y-%m-%d %H:%M:%S.%f")
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0',
                'id_planta': 'planta0',
                'id_grupo_maquina': 'grupo0', 'id_maquina': 'maquina0',
                'ano': '2017',
                'mes': '7', 'id_produccion': 'prod02', 'id_articulo': 'art02',
                'descr_articulo': 'articulo prueba 2',
                'fechahora_inicial': fromDateTimeStr,
                'fechahora_final': toDateTimeStr, 'num_horas': '48',
                'cantidad_producir': '100', 'tasa_esperada': '1.56',
                'velocidad_esperada': '1.35',
                'create_date': datetimeStr, 'last_updttm': datetimeStr}

        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'orden_produccion_planeada/0/'
        if not token:
            response = requests.put(url, data=jsonText,
                                    auth=('admin', 'admin2018'))
        else:
            response = requests.put(url, data=jsonText,
                                    headers=token)
        self.assertEqual(response.status_code, 200)


class ParadaPlaneadaViewTest(TestCase):
    """
       First it deletes all orden produccion planeada with id (compania0, sede0, planta0), which is the one chosen for testing
    """

    def test_view_a_detail_delete(self, token=None):
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0',
                'id_planta': 'planta0',
                'id_grupo_maquina': 'grupo0', 'id_maquina': 'maquina0',
                'ano': '2017',
                'mes': '5', 'id_produccion': 'prod01', 'fechahora_inicial': '',
                'fechahora_final': '', 'create_date': '', 'last_updttm': ''}

        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'parada_planeada/0/'
        if not token:
            response = requests.delete(url, data=jsonText,
                                       auth=('admin', 'admin2018'))
        else:
            response = requests.delete(url, data=jsonText,
                                       headers=token)
        self.assertEqual(response.status_code, 204)

    def test_view_b_post(self, token=None):
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0',
                'id_planta': 'planta0',
                'id_grupo_maquina': 'grupo0', 'id_maquina': 'maquina0',
                'ano': '2017',
                'mes': '5', 'id_produccion': 'prod01',
                'fechahora_inicial': '2017-05-22 12:00:00.000',
                'fechahora_final': '2017-05-22 14:00:00.000',
                'create_date': '2017-05-22 00:00:00.000',
                'last_updttm': '2017-05-22 00:00:00.000'}

        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'parada_planeada/'
        if not token:
            response = requests.post(url, data=jsonText,
                                     auth=('admin', 'admin2018'))
        else:
            response = requests.post(url, data=jsonText,
                                     headers=token)
        self.assertEqual(response.status_code, 201)

    def test_view_c_list_get(self, token=None):
        url = host + port + url_prefix + 'parada_planeada/'
        if not token:
            response = requests.get(url, auth=('admin', 'admin'))
        else:
            response = requests.get(url, headers=token)
        self.assertEqual(response.status_code, 200)

    def test_view_d_detail_get(self, token=None):
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0',
                'id_planta': 'planta0',
                'id_grupo_maquina': 'grupo0', 'id_maquina': 'maquina0',
                'ano': '2017',
                'mes': '5', 'id_produccion': 'prod01', 'fechahora_inicial': '',
                'fechahora_final': '', 'create_date': '', 'last_updttm': ''}

        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'parada_planeada/0/'
        if not token:
            response = requests.get(url, data=jsonText,
                                    auth=('admin', 'admin2018'))
        else:
            response = requests.get(url, data=jsonText,
                                    headers=token)
        self.assertEqual(response.status_code, 200)

    def test_view_e_detail_put(self, token=None):
        dict = {'id_compania': 'compania0', 'id_sede': 'sede0',
                'id_planta': 'planta0',
                'id_grupo_maquina': 'grupo0', 'id_maquina': 'maquina0',
                'ano': '2017',
                'mes': '5', 'id_produccion': 'prod01',
                'fechahora_inicial': '2017-05-22 12:00:00.000',
                'fechahora_final': '2017-05-22 14:00:00.000',
                'create_date': '2017-05-22 00:00:00.000',
                'last_updttm': '2017-05-22 00:00:00.000'}

        jsonText = json.dumps(dict)
        url = host + port + url_prefix + 'parada_planeada/0/'
        if not token:
            response = requests.put(url, data=jsonText,
                                    auth=('admin', 'admin2018'))
        else:
            response = requests.put(url, data=jsonText,
                                    headers=token)
        self.assertEqual(response.status_code, 200)


def load_metamodel_data():
    url = host + port + '/api/auth/'
    data = {'username': 'admin', 'password': 'admin2018'}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        token = response.json()
        headers = {'Authorization': 'Token ' + token['token']}

        compania = CompaniaViewTest()
        compania.test_view_a_detail_delete(headers)
        compania.test_view_b_post(headers)

        sede = SedeViewTest()
        sede.test_view_a_detail_delete(headers)
        sede.test_view_b_post(headers)

        planta = PlantaViewTest()
        planta.test_view_a_detail_delete(headers)
        planta.test_view_b_post(headers)

        razon_parada = RazonesParadaViewTest()
        razon_parada.test_view_a_detail_delete(headers)
        razon_parada.test_view_b_post(headers)

        grupo_maquina = GrupoMaquinaViewTest()
        grupo_maquina.test_view_a_detail_delete(headers)
        grupo_maquina.test_view_b_post(headers)

        maquina = MaquinaViewTest()
        maquina.test_view_a_detail_delete(headers)
        maquina.test_view_b_post(headers)


def load_production_plan():
    production_plan = PlanProductionViewTest()
    production_plan.test_view_a_detail_delete()
    production_plan.test_view_b_post()

    orden_produccion = OrdenProduccionPlaneadaViewTest()
    orden_produccion.test_view_a_detail_delete()
    orden_produccion.test_view_b_post()

    # parada_planeada = ParadaPlaneadaViewTest()
    # parada_planeada.test_view_a_detail_delete()
    # parada_planeada.test_view_b_post()
