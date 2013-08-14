'''
Created on 08.07.2013

@author: vau
'''

import core
import time

if __name__ == '__main__':
    
    print('Starting Core')
    c    = core.Core()
    core.setCoreInstance(c)
    c.start()
    
    tmInstance          = c.getInstance('TASK_MANAGER')
    schedulerInstance   = c.getInstance('SCHEDULER')
    for schtask in schedulerInstance.getNotInitiatedDefaultTasks():
        tmInstance.new_task('addScheduledTask', schtask)     
    
    try:
        print('LEMON AGENT')
        while True:
            time.sleep(0.1)           
    except KeyboardInterrupt:
        c.stop()
        