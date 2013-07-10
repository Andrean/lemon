'''
Created on 08.07.2013

@author: vau
'''

import threading
import time
import json

MASK    = "contractor_layer"

class Layer(threading.Thread):
    '''
    Через данный класс как уровень осуществляются все обращения к вспомогательным скриптам - контракторам
    Также данный класс управляет запуском контракторов, хранит всю информацию о запущенных контракторах
    '''


    def __init__(self, _logger, _config, _storageInstance):
        '''
        Constructor
        '''
        self._logger    = _logger
        self._config    = _config
        self._storage   = _storageInstance
        self._contractors   = {}
        self._running   = False
    
        threading.Thread.__init__(self)
        self._logger.info("Contractor layer initialized")
        
    def run(self):
        
        self._running   = True
        self._logger.info("Layer started")
        while self._running:
            time.sleep(0.01) 
        self._logger.info("Layer stopped")
        
    def waitReady(self):
        while self._running is not True:
            time.sleep(0.1)
            
    def quit(self):
        self._running   = False
        
    def _load(self):
        try:
            value   = self._storage.readStr(MASK)
            if value is not None:
                self._contractors   = json.loads(value)
        except Exception as e:
            self._logger.exception("Error occured in _load", e)           