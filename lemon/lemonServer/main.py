'''
Created on 13.06.2013

@author: vau
'''
import core

if __name__ == '__main__':

    c = core.Core()
    core.setCoreInstance(c)
    c.start()
    print(c._instances)
    
    '''
    
    # new storage instance
    stEntities          = storageManagerInstance.getInstance()
    if stEntities is None:
        mainLogger.error('stEntities is None. Exiting')
        exit(1)

    stEntities.set_default_collection('entities')
    # testing storage instance
    print(stEntities.getCollections())
    print([v for v in stEntities.find({'name':'computer2'})])
    # create task handlers
    #storeTaskHandler        = task.StoreTaskHandler('storeTaskHandler',storageManagerInstance)
    
    #connect task handlers to task manager
 #   taskManager.connectHandler(storeTaskHandler)
    
    #shutdown agent listener
    try:
        while(True):
            time.sleep(0.5)
    except KeyboardInterrupt:
        agentServerInstance.shutdownListener()
 #       taskManager.shutdown()
        logging.shutdown()
    ''' 