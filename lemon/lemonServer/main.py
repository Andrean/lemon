'''
Created on 13.06.2013

@author: vau
'''
import server
import webInterfaceListener
import main_config
import configparser
import logging.config
import task
import time
import basicStorage
import StorageManager
import exception.lemonException
from task import TaskManager

if __name__ == '__main__':
    
    # set up configure 
    config  = configparser.ConfigParser()
    config.read(main_config.CONFIG_FILE)
    if len(config.sections()) < 1:
        main_config.writeDefaultConfig(config)
    logging.config.fileConfig(config['LOGGING']['file'])
    
    #create loggers
    mainLogger              = logging.getLogger('MAIN')
    taskLogger              = logging.getLogger('TASK')
    serverLogger            = logging.getLogger('MAIN')
    mainStorageLogger       = logging.getLogger('STORAGE')
    # creating task manager instance
    taskManager             = TaskManager(taskLogger, config)
    taskManager.start()
    # creating storage instances
    try:
        #mainStorageInstance = basicStorage.Storage('.storage', mainStorageLogger, config['STORAGE'])
        storageManagerInstance  = StorageManager.StorageManager(mainStorageLogger, config['STORAGE']); 
        mainLogger.info('main storage instance created')        
    except exception.lemonException.StorageNotCreatedException as storageException:
        mainLogger.error('storage not created {}'.format(storageException))
        logging.shutdown()
        exit(0)
    
    # create task handlers
    storeTaskHandler        = task.StoreTaskHandler('storeTaskHandler',storageManagerInstance)
    
    #connect task handlers to task manager
    taskManager.connectHandler(storeTaskHandler)
    
    # creating interface instances
    agentServerInstance     = server.Server(20, serverLogger, config, taskManager);
    httpInterfaceInstance   = webInterfaceListener.httpListener();
    
    #starting instances
    storageManagerInstance.start();
    agentServerInstance.start();
    httpInterfaceInstance.start();
    
    #shutdown agent listener
    try:
        while(True):
            time.sleep(0.5)
    except KeyboardInterrupt:
        agentServerInstance.shutdownListener()
        taskManager.shutdown()
        logging.shutdown()