'''
Created on 10.07.2013

@author: vau
'''

import threading
import time

WAIT_POLL   = 0.01

class BaseAgentLemon(threading.Thread):
 
    def __init__(self, _logger, _config):
        self._logger    = _logger
        self._config    = _config
        self._running   = False
        threading.Thread.__init__(self)
        
    def run(self):
        pass
    
    def waitReady(self):
        while self._running is not True:
            time.sleep(WAIT_POLL)
    
    def quit(self):
        self._running   = False
           
     
        