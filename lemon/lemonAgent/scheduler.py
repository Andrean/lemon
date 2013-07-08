'''
Created on 08.07.2013

@author: vau
'''
import threading

class Scheduler(threading.Thread):
    '''
    classdocs
    '''


    def __init__(self, _logger, _config):
        '''
        Constructor
        '''
        self._logger    = _logger
        self._config    = _config
        
        threading.Thread.__init__(self)
        
    def run(self):
        pass
        