'''
Created on 08.07.2013

@author: vau
'''

import core


if __name__ == '__main__':
    
    print('Starting Core')
    c    = core.Core()
    core.setCoreInstance(c)
    c.start()
    
    tmInstance          = c.getInstance('TASK_MANAGER')
    schedulerInstance   = c.getInstance('SCHEDULER')
    for schtask in schedulerInstance.getNotInitiatedDefaultTasks():
        tmInstance.new_task('addScheduledTask', schtask)     
    
    #script  = 'print("Testing!)'
    #contrLayer.addContractor('one_test', script)
    #contrLayer.startContractors(['one_test'])
    
    '''
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
    '''    
        
        