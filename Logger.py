# ------------------------Dependencies----------------------------------------------------------------------------------
import logging
from datetime import datetime
import string

# ------------------------Logger Class----------------------------------------------------------------------------------


class Logger:
    def __init__(self):
        logging.basicConfig(filename='Log.log', level=logging.INFO)

# ------------------------Append function-------------------------------------------------------------------------------
# Appends message to log file with a timestamp.

    def append(self, level: string, message: string):
        if level == 'debug':
            logging.debug("[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] - " + message)
        if level == 'info':
            logging.info("[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] - " + message)
        if level == 'warning':
            logging.warning("[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] - " + message)
