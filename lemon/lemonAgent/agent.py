'''
Created on 08.07.2013

@author: vau
'''
VERSION = '0.1.1'

import core
import time


if __name__ == '__main__':
    
    print('Starting Core')
    c    = core.Core()
    core.setCoreInstance(c)   
    c.start()
    c.renewVersion(VERSION)
    tmInstance          = c.getInstance('TASK_MANAGER')
    schedulerInstance   = c.getInstance('SCHEDULER')
    for schtask in schedulerInstance.getNotInitiatedDefaultTasks():
        tmInstance.new_task('addScheduledTask', schtask)     
    
    try:
        print("""
        ##########################################################
        #                                                        #
        #        ##     #####  ##    ##  ######  ##   ##         # 
        #        ##     ##     ###  ###  ##  ##  ###  ##         # 
        #        ##     ####   ## ## ##  ##  ##  ## # ##         #
        #        ##     ##     ##    ##  ##  ##  ##  ###         #
        #        #####  #####  ##    ##  ######  ##   ##         #
        #                                                        #
        #********************************************************#
        #                        AGENT                           # 
        #                                                        #
        ##########################################################        
        """)
        while True:
            time.sleep(1)           
    except KeyboardInterrupt:
        c.stop()
        