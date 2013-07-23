'''
Created on 18.07.2013

@author: vau
'''

import logging.config
import storagemanager
import task_manager
import scheduler.scheduler as scheduler
import server
import os
import configparser


CONFIG_PATH = 'conf'
CONFIG_FILE = CONFIG_PATH + '/server.conf'

COMPONENTS          = ['TASK_MANAGER', 'SERVER','SCHEDULER']
SERVER_COMPONENTS   = {'STORAGE': storagemanager.StorageManager, 'TASK_MANAGER': task_manager.TaskManager, 'SERVER': server.Server, 'SCHEDULER': scheduler.Scheduler} 
TM_HANDLERS         = {'store': task_manager.StoreTaskHandler}

CORE_INSTANCE   = None


def getCoreInstance():
    return CORE_INSTANCE

def setCoreInstance(instance):
    global CORE_INSTANCE
    CORE_INSTANCE = instance
    
def getInstanceTemplate(name):
    t   = { 'name': name, 'instance': None, 'start_timestamp': None, 'end_timestamp': None, 'state': "noninit", 'threads': 0, 'errors': 0 }
    return t

class Core(object):
    '''
    Root module which contains all info about server and has all running instances
    and open descriptors
    '''


    def __init__(self):
        self._instances = {}
        self._stat      = {}        
        self._loggers   = {}
        self._config    = {}
        self._clogger   = self.__initCLogger() 
        
    def __initCLogger(self):
        name    = 'CORE'
        core_format  = '%(asctime)s\t %(name)s\t%(levelname)s\t%(message)s'
        coreFormatter       = logging.Formatter(core_format)
        consoleHandler      = logging.StreamHandler()
        consoleHandler.setLevel(logging.DEBUG)
        consoleHandler.setFormatter(coreFormatter)
        self._clogger    = logging.getLogger(name)
        self._clogger.addHandler(consoleHandler)
        self._clogger.setLevel(logging.DEBUG)  
        
    def __initInstance(self, name, cls):
        if name:
            self._instances[name]   = getInstanceTemplate(name)
            t = cls(self._loggers[name], self._config[name], self._instances[name])
            self._instances[name]['instance']   = t
            self._clogger.debug('init '+str(name))   
    
    def _initInstances(self):
        for name, cls in SERVER_COMPONENTS.items():
            self.__initInstance(name, cls)
            
    def _startStorageManager(self):
        name            = 'STORAGE'
        instance        = self._instances[name]['instance'] 
        instance.start()
        instance.waitReady()
        self._clogger.info('start '+str(name))
        
    def _startInstances(self):
        for name in COMPONENTS:
            self._instances[name]['instance'].start()
            self._clogger.info('start '+str(name))
        
    def _initLoggers(self):
        for name in SERVER_COMPONENTS.keys():
            self._loggers[name] = logging.getLogger(name)
        self._clogger   = logging.getLogger('CORE')
        
    def _connectHandlers(self):
        tmInstance  = self._instances['TASK_MANAGER']['instance']
        for hndl_name, handler in TM_HANDLERS.items():
            hndl    = handler(hndl_name)
            tmInstance.connectHandler(hndl)
    
    def _initConfig(self):
        def writeDefaultConfig(config):
            config.add_section('STORAGE')
            storageConfig                   = config['STORAGE']
            storageConfig['data_path']      = 'data/storage/'
            config.add_section('TASK_MANAGER')
            config.add_section('SERVER')
            config.add_section('SCHEDULER')
            config.add_section('LOGGING')
            loggingConfig                   = config['LOGGING']
            loggingConfig['file']           = CONFIG_PATH + '/logging.conf'
            if not os.path.exists(CONFIG_PATH):
                os.makedirs(CONFIG_PATH)
            with open(CONFIG_FILE,'w') as configFile:        
                config.write(configFile)
        
        self._config  = configparser.ConfigParser()
        config  = self._config
        config.read(CONFIG_FILE)
        if len(config.sections()) < 1:
            writeDefaultConfig(config)
        logging.config.fileConfig(config['LOGGING']['file'])
    
    def getInstance(self, name):
        return self._instances[name]['instance']
               
    def start(self):
        self._initConfig()
        self._initLoggers()
        self._initInstances()
        self._startStorageManager()
        self._startInstances()  
        self._connectHandlers()  
                            
        