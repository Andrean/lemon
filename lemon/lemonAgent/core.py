'''
Created on 17.07.2013

@author: vau
'''
import scheduler.scheduler as scheduler
import taskmanager
import storage
import interface
import contractorLayer
import entity_manager
import configparser
import logging.config
import os
import uuid
import threading
import time
import yaml

# core version
VERSION     = '1.0.1'
# configuration base parameters
CONFIG_PATH = 'conf'
CONFIG_FILE = CONFIG_PATH + '/agent.yaml'

# Do not change order of instances. Important: storage must be first, task_manager - second
COMPONENTS  = ['TASK_MANAGER', 'SCHEDULER', 'INTERFACE', 'CONTRACTOR','ENTITY_MANAGER']
AGENT_COMPONENTS   = {  'STORAGE': storage.Storage, 
                        'TASK_MANAGER': taskmanager.TaskManager, 
                        'SCHEDULER': scheduler.Scheduler, 
                        'INTERFACE': interface.XMLRPC_Client, 
                        'CONTRACTOR': contractorLayer.Layer ,
                        'ENTITY_MANAGER': entity_manager.EntityManager    }
core_instance   =    None

def setCoreInstance(_core):
    global core_instance
    core_instance  = _core
    
def getCoreInstance():
    return core_instance

def getTemplate():
    t   =  {    'instance': None, 
                'state': 'not', 
                'start_timestamp': None,
                'end_timestamp': None, 
                'threads': 0, 
                'exceptions': 0, 
                'errors': 0 }
    return t

def getStatTemplate():
    t   = {'agent': {'__id': None, 'start_timestamp': None, 'threads': 0, 'instances': [], 'version': 0}}
    return t

class Core(object):
    '''
    Global object which has all information about agent: running instances, upload time, 
    '''


    def __init__(self):
        self._running    = False
        self._stat       = {}
        self._instances  = {}
        self._loggers    = {}
        self._config     = {}
        self.__initCoreLogger()
        self._corelogger.info('core started')
        self.agentVersion   = 0
    
    def __initCoreLogger(self):
        name    = 'CORE'
        core_format  = '%(asctime)s\t %(name)s\t%(levelname)s\t%(message)s'
        coreFormatter       = logging.Formatter(core_format)
        consoleHandler      = logging.StreamHandler()
        consoleHandler.setLevel(logging.DEBUG)
        consoleHandler.setFormatter(coreFormatter)
        self._corelogger    = logging.getLogger(name)
        self._corelogger.addHandler(consoleHandler)
        self._corelogger.setLevel(logging.DEBUG)        
        
    def __initInstance(self, name, cls):
        self._corelogger.info('initiate instance "{0}"'.format(name))
        self._instances[name]   = getTemplate()
        self._instances[name]['instance']   = cls(self._loggers[name], self._config[name], self._instances[name])
        
    def __initAgentID(self):
        if self._stat['agent']['__id'] is None:
            agent_id = self._instances['STORAGE']['instance'].readStr('agent_id')
            if agent_id is None:
                agent_id    = str(uuid.uuid4())
                self._instances['STORAGE']['instance'].writeItem('agent_id', agent_id )
            self._stat['agent']['__id'] = agent_id
            
    def _initInstances(self):
        self._corelogger.info('initiate agent components')
        for name, cls in AGENT_COMPONENTS.items():
            self.__initInstance(name, cls)
    
    def _initStat(self):
        self._stat  = getStatTemplate()
        
    def _updateStat(self):
        self.__initAgentID()
        if self._stat['agent']['start_timestamp'] is None:
            self._stat['agent']['start_timestamp'] = time.time()
        threads = threading.active_count()
        self._stat['agent']['threads']  = threads
            
    def _startInstances(self):
        self._corelogger.info('start instances')
        for name in COMPONENTS:
            self._instances[name]['instance'].start()
            self._instances[name]['instance'].waitReady()
            self._corelogger.info('start "{0}"'.format(name))
                
    def _startStorage(self):
        name    = 'STORAGE'
        self._instances[name]['instance'].start()
        self._instances[name]['instance'].waitReady()
        self._corelogger.info('start "{0}"'.format(name))
        
    def _initLoggers(self):
        self._corelogger.info('initiate all loggers')
        for name in AGENT_COMPONENTS.keys():
            self._loggers[name] = logging.getLogger(name)
    
    def _loadConfig(self):
        def writeDefaultConfig():
            config  = {}
            config['storage'] = {
                'data_path': 'data/storage'
            }
            config['scheduler'] = {}
            config['task_manager'] = {}
            config['interface'] = {
                'server': 'dev-lemon:8080'
            }
            config['contractor'] = {}
            config['entity_manager'] = {}
            config['logging'] = {
                'file': 'conf/logging.yaml'
            }
            
            #config.add_section('STORAGE')
            #storageConfig                   = config['STORAGE']
            #storageConfig['data_path']      = 'data/storage/'
            #config.add_section('SCHEDULER')
            #config.add_section('TASK_MANAGER')
            #config.add_section('INTERFACE')
            #config.add_section('CONTRACTOR')
            #config.add_section('ENTITY_MANAGER')
            #interfaceConfig                 = config['INTERFACE']
            #interfaceConfig['xmlrpc_server_addr'] = 'localhost'
            #interfaceConfig['xmlrpc_server_port'] = '8000' 
            #config.add_section('LOGGING')
            #loggingConfig                   = config['LOGGING']
            #loggingConfig['file']           = CONFIG_PATH + '/logging.conf'
            
            os.makedirs(CONFIG_PATH,exist_ok=True)
            yaml.dump(config, open(CONFIG_FILE,'w'))
            return config
        
        #self._config  = configparser.ConfigParser()
        if os.path.exists(CONFIG_FILE):
            self._config = yaml.load(open(CONFIG_FILE))
        else:
            self._config    = writeDefaultConfig()
        for key in ['ENTITY_MANAGER','TASK_MANAGER','SCHEDULER','CONTRACTOR']:
            if not self._config.__contains__(str.lower(key)):
                self._config[str.lower(key)] = {}
        keys    = [x for x in self._config.keys()]
        for key in keys:
            self._config[str.upper(key)]    = self._config[key]
        log_config_file = os.path.abspath(self._config['logging']['file'])
        logging_config  = yaml.load(open(log_config_file))
        for item in logging_config['handlers'].values():
            if item.__contains__('filename'):
                os.makedirs(os.path.dirname(item['filename']),exist_ok=True)
        logging.config.dictConfig(logging_config)        
    
    def getInstance(self, name):
        try:
            return self._instances[name]['instance']
        except KeyError as e:
            self._corelogger.error('Cannot get instance "{0}"'.format(str(e)))
            
    def terminateInstances(self):
        for k in COMPONENTS.reverse():
            self._instances[k]['instance'].quit()
    
    def getItem(self, item):
        try:
            return self._stat[item]
        except KeyError as e:
            self._corelogger.error('Cannot get item "{0}"'.format(str(e)))
            
    def updateStat(self):
        self._updateStat()
    
    def getStat(self):        
        self._stat['agent']['instances'] = []
        for k, v in self._instances.items():
            self._stat['agent']['instances'].append( {'name': k,'state': v['state'], 'threads': v['threads'], 'exceptions':v['exceptions'],'errors': v['errors']} )
        self._stat['agent']['version']  = self.agentVersion
        return self._stat
        
    def renewVersion(self, _version):
        self.agentVersion = _version
        
    def is_alive(self):
        return self._running
        
    def start(self):
        self._running = True
        self._loadConfig()
        self._initStat()
        self._initLoggers()
        self._initInstances()
        self._startStorage()
        self._updateStat()
        self._startInstances()
        
    def stop(self):
        self.terminateInstances()
        self._running   = False
        
    
    