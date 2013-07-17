'''
Created on 10.07.2013

@author: vau
'''

import threading
import time

WAIT_POLL   = 0.01


def changeStateDecorator(f):
    def wrapper(self):
        self.__changeInstanceState('started')
        f(self)
        self.__changeInstanceState('stopped')
    return wrapper
    
class BaseAgentLemon(threading.Thread):
 
    def __init__(self, _logger, _config, _info):
        self._logger    = _logger
        self._config    = _config
        self._info      = _info
        self._running   = False
        threading.Thread.__init__(self)
        self.__changeInstanceState('initiated')
        
    @changeStateDecorator    
    def run(self):
        pass
    
    def waitReady(self):
        while self._running is not True:
            time.sleep(WAIT_POLL)
            
    def _setReady(self):
        self._running   = True
        self.__changeInstanceState('running')
        
    def quit(self):
        self.__changeInstanceState('stopping')
        self._running   = False
           
    def __changeInstanceState(self, new_state):
        last_state  = self._info['state']
        self._info[last_state+'_end']    = time.time()
        self._info['state'] = new_state
        self._info[new_state+'_start']   = time.time()
        