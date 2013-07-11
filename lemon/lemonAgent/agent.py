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
import contractorLayer
import uuid


CONFIG_PATH = 'conf'
CONFIG_FILE = CONFIG_PATH + '/agent.conf'

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

if __name__ == '__main__':
    
    FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
    logging.basicConfig(format=FORMAT)
    
    config  = configparser.ConfigParser()
    logging.info("Try to read config file...")
    config.read(CONFIG_FILE)
    if len(config.sections()) < 1:
        logging.info("Configuration file not found. Creating default config file...")
        writeDefaultConfig(config)
        logging.info("Configuration file was created successfully in {0}".format(CONFIG_FILE))
    logging.config.fileConfig(config['LOGGING']['file'])
    
    logging.info("Getting other loggers from configuration file")
    logger      = logging.getLogger('MAIN')
    tmLogger    = logging.getLogger('TASK_MANAGER')
    schLogger   = logging.getLogger('SCHEDULER')
    stLogger    = logging.getLogger('STORAGE')
    faceLogger  = logging.getLogger('INTERFACE')
    contrLogger = logging.getLogger('CONTRACTOR')
    
    logger.info('Loggers were getting')
    # creating and starting main instances
    storageInstance  = storage.Storage(stLogger, config['STORAGE'])
    logger.info('Storage was created')
    storageInstance.start()
    logger.info('Storage instance started')
    logger.info('Getting agent id from storage...')
    agentID          = storageInstance.readStr('agent_id')
    if agentID is None:
        agentID      = uuid.uuid4()
        storageInstance.writeItem('agent_id', str(agentID))
        logger.info('Agent id not found. New id was generated. Agent ID: {0}'.format(agentID))
    else:
        logger.info('Agent ID is {0}'.format(agentID))
        
    tmInstance       = taskmanager.TaskManager(tmLogger, config['TASK_MANAGER'])
    tmInstance.start()
    logger.info('Task manager instance was created and started')
    
    contrLayer       = contractorLayer.Layer(contrLogger, config['CONTRACTOR'], storageInstance)
    logger.info('Contractors Layer was created')
    schedulerInstance    = scheduler.Scheduler(schLogger, config['SCHEDULER'], storageInstance, tmInstance)
    logger.info('Scheduler was created')
    xmlrpc_client    = interface.XMLRPC_Client(faceLogger, config['INTERFACE'], agentID, tmInstance)
    logger.info('XMLRPC Client was created')    
    tmInstance.storageInstance      = storageInstance
    tmInstance.interfaceInstance    = xmlrpc_client
    tmInstance.scheduler            = schedulerInstance
    
    logger.info('Starting instances...')
    def logStarting(instance, instanceName):
        instance.start()
        logger.info('Starting {0}'.format(instanceName))
        instance.waitReady()
        logger.info('{0} started'.format(instanceName))
    logStarting(contrLayer, 'Contractor Layer')
    logStarting(xmlrpc_client, 'XMLRPC Client')
    logStarting(schedulerInstance, 'Scheduler')
    
   
    if(schedulerInstance.getScheduledTask('refresh') is None):
        refreshServer = {  'func': 'refresh',
                           'name': 'refresh',
                           'interval': 1,
                           'start_time': None,
                           'kwargs': {}
                           }
        tmInstance.new_task('addScheduledTask', refreshServer)
        
    #schtask = {'func':'testPrint', 'name':'templ_task6', 'start_time': None, 'interval': 10,  'kwargs': {'los':'', 't':True}}
    #tmInstance.new_task('addScheduledTask', schtask)
    
    #script  = 'print("Testing!)'
    #contrLayer.addContractor('one_test', script)
    #contrLayer.startContractors(['one_test'])
    
    
    try:
        logger.info('LEMON AGENT STARTED')
        completed   = []
        while True:
            time.sleep(0.1)
            contractors  = contrLayer.getStat()
            for k,v in contractors.items():
                if v['state'] == contractorLayer.STATE.STOPPED and (k not in completed):
                    completed.append(k)
                    print(contractors[k])           
    except KeyboardInterrupt:
        schedulerInstance.quit()
        tmInstance.quit()
        storageInstance.quit()
        
        
        