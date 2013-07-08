'''
Created on 08.07.2013

@author: vau
'''
import threading

class TaskManager(threading.Thread):
    '''
    classdocs
    '''

    def __init__(self, _logger, _config):
        self._logger    = _logger
        self._config    = _config
        threading.Thread.__init__(self)
        
    def run(self):
        pass