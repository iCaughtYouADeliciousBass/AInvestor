import os
import logging
from datetime import datetime
import string


class Logger:
    def __init__(self):
        logging.basicConfig(filename='Log.log', level=logging.INFO)
        #logging.info('[{}] - Logging started'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))

    def append(self, level: string, message: string):
        if level == 'debug':
            logging.debug("[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] - " + message)
        if level == 'info':
            logging.info("[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] - " + message)
        if level == 'warning':
            logging.warning("[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] - " + message)
