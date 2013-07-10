'''
Created on 08.07.2013

@author: vau
'''

import configparser
import logging.config
import os
import storage
import taskmanager
import interface
import scheduler
import time


CONFIG_PATH = 'conf'
CONFIG_FILE = CONFIG_PATH + '/agent.conf'

def writeDefaultConfig(config):
    config.add_section('STORAGE')
    storageConfig                   = config['STORAGE']
    storageConfig['data_path']      = 'data/storage/'
    config.add_section('SCHEDULER')
    config.add_section('TASK_MANAGER')
    config.add_section('INTERFACE')
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

if __name__ == '__main__':
    
    config  = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    if len(config.sections()) < 1:
        writeDefaultConfig(config)
    logging.config.fileConfig(config['LOGGING']['file'])
    
    logger      = logging.getLogger('MAIN')
    tmLogger    = logging.getLogger('TASK_MANAGER')
    schLogger   = logging.getLogger('SCHEDULER')
    stLogger    = logging.getLogger('STORAGE')
    faceLogger  = logging.getLogger('INTERFACE')
    
    # creating and starting main instances
    storageInstance  = storage.Storage(stLogger, config['STORAGE'])
    storageInstance.start()
    #xmlrpc_client    = interface.XMLRPC_CLient()
    #xmlrpc_client.start()
    
    tmInstance       = taskmanager.TaskManager(tmLogger, config['TASK_MANAGER'])
    tmInstance.start()
    
    schedulerInstance    = scheduler.Scheduler(schLogger, config['SCHEDULER'], storageInstance, tmInstance)
    schedulerInstance.start()
    
    tmInstance.storageInstance  = storageInstance
    tmInstance.scheduler        = schedulerInstance
    
    
    schedulerInstance.waitReady()
    
    schtask = {'func':'testPrint', 'name':'templ_task6', 'start_time': None, 'interval': 10,  'kwargs': {'los':'', 't':True}}
    tmInstance.new_task('addScheduledTask', schtask)
    
        
        