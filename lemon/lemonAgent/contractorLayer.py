'''
Created on 08.07.2013

@author: vau
'''

import threading

class Layer(threading.Thread):
    '''
    classdocs
    '''


    def __init__(self, _logger, _config):
        '''
        Constructor
        '''
        self._logger    = _logger
        self._config    = _config
    
    def run(self):
        pass
        