from django_q.tasks import async
from django.http import HttpResponse, JsonResponse

import logging
import os
import logging.handlers

# Get an instance of a logger
LOG_FILENAME = 'iotsettings.log'

# Check if log exists and should therefore be rolled
needRoll = os.path.isfile(LOG_FILENAME)

logger = logging.getLogger('tasks')

fh = logging.handlers.RotatingFileHandler(LOG_FILENAME, backupCount=5)
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

def putReasonCode(json_data):
    url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
    url = url + defaults.CONTEXT_ROOT + '/'
    url = url + 'ReasonCode' + '/' + str(json_data['id_compania'] + 
                                         json_data['id_sede'] + 
                                         json_data['id_planta'] + 
                                         json_data['id_razon_parada'] )
    try:
        r = requests.put(url, data = json_data)
    except requests.exceptions.RequestException as e:
        logger.error(e)
        raise e


def delReasonCode(json_data):
    url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
    url = url + defaults.CONTEXT_ROOT + '/'
    url = url + 'ReasonCode' + '/' + str(json_data['id_compania'] + 
                                         json_data['id_sede'] + 
                                         json_data['id_planta'] + 
                                         json_data['id_razon_parada'] )
    try:
        r = requests.delete(url, data = json_data)
    except requests.exceptions.RequestException as e:
        logger.error(e)
        raise e

def putActivityRegister(json_data):
    url = defaults.JAVA_CONFIGURATION_SERVER + ':' + str(defaults.PORT) + '/'
    url = url + defaults.CONTEXT_ROOT + '/'
    url = url + '/Register/ActivityRegister' + '/'
    try:
        r = requests.put(url, data = json_data)
    except requests.exceptions.RequestException as e:
        logger.error(e)
        raise e

