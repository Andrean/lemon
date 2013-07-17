'''
Created on 17.07.2013

@author: vau
'''
import scheduler.scheduler as scheduler
import taskmanager
import storage
import interface
import contractorLayer
import configparser
import logging.config
import os

# configuration base parameters
CONFIG_PATH = 'conf'
CONFIG_FILE = CONFIG_PATH + '/agent.conf'

# Do not change order of instances. Important: storage must be first, task_manager - second
AGENT_COMPONENTS   = {  'storage': storage.Storage, 
                        'task_manager': taskmanager.TaskManager, 
                        'scheduler': scheduler.Scheduler, 
                        'interface': interface.XMLRPC_Client, 
                        'contractor': contractorLayer.Layer     }

instance_info_template  = { 'instance': None, 
                            'state': 'not', 
                            'start_timestamp': None,
                            'end_timestamp': None, 
                            'threads': 0, 
                            'exceptions': 0, 
                            'errors': 0}


class Core(object):
    '''
    Global object which has all information about agent: running instances, upload time, 
    '''


    def __init__(self):
        self._stat       = {}
        self._instances  = {}
        self._loggers    = {}
        self._config     = {}
        self.__initCoreLogger()
    
    def __initCoreLogger(self):
        name    = 'CORE'
        core_format  = '%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s'
        coreFormatter       = logging.Formatter(core_format)
        consoleHandler      = logging.StreamHandler()
        consoleHandler.setLevel(logging.DEBUG)
        consoleHandler.setFormatter(coreFormatter)
        self._corelogger    = logging.getLogger(name)
        self._corelogger.addHandler(consoleHandler)
        self._corelogger.setLevel(logging.DEBUG)        
        
    def __initInstance(self, name, cls):
        self._corelogger.info('initiate instance "{0}"'.format(name))
        self._instances[name]   = instance_info_template
        self._instances[name]['instance']   = cls(self._loggers[name], self._config[name], self._instances[name])
        
    def _initInstances(self):
        self._corelogger.info('initiate agent components')
        for name, cls in AGENT_COMPONENTS.items():
            self.__initInstance(name, cls)
            
    def _startInstances(self):
        self._corelogger.info('start instances')
        for name in AGENT_COMPONENTS.keys():
            self._instances[name]['instance'].start()
    
    def _initLoggers(self):
        self._corelogger.info('initiate all loggers')
        for name in AGENT_COMPONENTS.keys():
            self._loggers[name] = logging.getLogger(name)
    
    def _loadConfig(self):
        def writeDefaultConfig(config):
            config.add_section('STORAGE')
            storageConfig                   = config['STORAGE']
            storageConfig['data_path']      = 'data/storage/'
            config.add_section('SCHEDULER')
            config.add_section('TASK_MANAGER')
            config.add_section('INTERFACE')
            config.add_section('CONTRACTOR')
            interfaceConfig                 = config['INTERFACE']
            interfaceConfig['xmlrpc_server_addr'] = 'localhost'
            interfaceConfig['xmlrpc_server_port'] = '8000' 
            config.add_section('CONTRACTOR')
            config.add_section('LOGGING')
            loggingConfig                   = config['LOGGING']
            loggingConfig['file']           = CONFIG_PATH + '/logging.conf'
            
            if not os.path.exists(CONFIG_PATH):
                os.makedirs(CONFIG_PATH)        
            
            with open(CONFIG_FILE,'w') as configFile:        
                config.write(configFile)
        
        config  = configparser.ConfigParser()     
        config.read(CONFIG_FILE)
        self._corelogger.info('load configuration')
        if len(config.sections()) < 1:
            self._corelogger.info('write default configuration to file')
            writeDefaultConfig(config)            
        logging.config.fileConfig(config['logging']['file'])
    
    def getInstance(self, name):
        pass
    
    def start(self):
        self._loadConfig()
        self._initLoggers()
        self._initInstances()
     
    
    