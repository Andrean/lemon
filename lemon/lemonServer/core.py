'''
Created on 18.07.2013

@author: vau
'''

import logging.config
import storagemanager
import task_manager
import entity_manager
import scheduler.scheduler as scheduler
import server
import os
import configparser
import yaml


CONFIG_PATH = 'conf'
#CONFIG_FILE = CONFIG_PATH + '/server.conf'
CONFIG_FILE = CONFIG_PATH + '/server.yaml'

COMPONENTS          = ['TASK_MANAGER', 'SERVER','SCHEDULER', 'ENTITY_MANAGER']
SERVER_COMPONENTS   = {'STORAGE': storagemanager.StorageManager, 'TASK_MANAGER': task_manager.TaskManager, 'SERVER': server.Server, 'SCHEDULER': scheduler.Scheduler, 'ENTITY_MANAGER': entity_manager.EntityManager} 
TM_HANDLERS         = {'store': task_manager.StoreTaskHandler, 'scheduler': task_manager.SchedulerTaskHandler}

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
            print(self._loggers)
            print(self._config)
            print(self._instances)
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
        def writeDefaultConfig(cfg = {}):
            cfg['STORAGE']  = {
                'data_path': 'data/storage/'
            }
            cfg['TASK_MANAGER'] = {}
            cfg['SERVER']   = {}
            cfg['SCHEDULER']= {}
            cfg['LOGGING']  = {
                'file': 'conf/logging.conf'
            }
            os.makedirs(CONFIG_PATH,exist_ok=True)
            yaml.dump(cfg, open(CONFIG_FILE,'w'))
            return cfg
            
        self._config    = {}
        if os.path.exists(CONFIG_FILE):
            self._config = yaml.load(open(CONFIG_FILE))
        else:
            self._config    = writeDefaultConfig()
        for key in ['ENTITY_MANAGER','TASK_MANAGER','SCHEDULER']:
            if not self._config.__contains__(key):
                self._config[key] = {}
        os.makedirs('logs',exist_ok=True)
        logging.config.fileConfig(self._config['LOGGING']['file'])
        
    def getInstance(self, name):
        return self._instances[name]['instance']
               
    def start(self):
        self._initConfig()
        self._initLoggers()
        self._initInstances()
        self._startStorageManager()
        self._startInstances()  
        self._connectHandlers()  
                            
        