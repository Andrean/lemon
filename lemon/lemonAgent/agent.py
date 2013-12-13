'''
Created on 08.07.2013

@author: vau
'''
VERSION = '0.1.2'

import core

if __name__ == '__main__':
    
    c    = core.Core()
    try:
        core.setCoreInstance(c)   
        c.start()
        c.renewVersion(VERSION)
        tmInstance          = c.getInstance('TASK_MANAGER')
        schedulerInstance   = c.getInstance('SCHEDULER')
        for schtask in schedulerInstance.getNotInitiatedDefaultTasks():
            tmInstance.new_task('addScheduledTask', schtask)   
    
    
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
        c.join()           
    except KeyboardInterrupt:
        pass
    finally:
        c.stop()