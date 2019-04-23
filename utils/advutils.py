import logging
from django.conf import settings

def get_logger(name):
    """
    Creates a logger object with the format
    :param name: the name of the logger
    :return: the logger object with format and handler
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    log_path = settings.LOG_PATH
    file_handler = logging.FileHandler(log_path + name + '.log')
    file_handler.setLevel(logging.INFO)
    formater = logging.Formatter('%(asctime)s %(name)s - %(lineno)s: %(levelname)s - %(message)s')
    file_handler.setFormatter(formater)
    logger.addHandler(file_handler)
    return logger