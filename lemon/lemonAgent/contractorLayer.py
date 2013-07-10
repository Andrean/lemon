'''
Created on 08.07.2013

@author: vau
'''

import time
import json
import lemon

MASK    = "contractor_layer"

class Layer(lemon.BaseAgentLemon):
    '''
    This class is layer where stored info about subprocesses as contractors, used to read perfomance counters
    '''


    def __init__(self, _logger, _config, _storageInstance):
        '''
        Constructor
        '''
        self._storage   = _storageInstance
        self._contractors   = {}
        lemon.BaseAgentLemon.__init__(self, _logger, _config)
        self._logger.info("Contractor layer initialized")
        
    def run(self):
        
        self._running   = True
        self._logger.info("Layer started")
        while self._running:
            time.sleep(0.01) 
        self._logger.info("Layer stopped")
        
    def addContractor(self):
        pass
    
    def removeContractor(self):
        pass 
    
    def getStat(self):
        pass
    
    def startContractors(self, contractor_list):
        pass
    
    def stopContractors(self, contractor_list):
        pass
    
    def _load(self):
        try:
            value   = self._storage.readStr(MASK)
            if value is not None:
                self._contractors   = json.loads(value)
        except Exception as e:
            self._logger.exception("Error occured in _load", e)           