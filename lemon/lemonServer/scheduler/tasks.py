'''
Created on 23.07.2013

Contains default scheduled tasks, which scheduled on start
@author: vau
'''
CMD = []

def add(task):
    CMD.append(task)
    
def formSchTask(func, name, interval, start_time=None, kwargs={}):
    _task    = {'func': func,
                'name': name,
                'interval': interval,
                'start_time': start_time,
                'kwargs': kwargs
                }
    return _task

add( formSchTask('clean_commands', 'Cleaning old commands', 60) )
add( formSchTask('remove_old_links', 'Delete old file virtual links', 60) )
#refreshServerStat   =   formSchTask('refreshServerStat', 'Refreshing server state and statistics', 10, None)
#checkManageUpdate   =   formSchTask('updateContractors', 'Check database for new update of commands and configuration', 10, None)
#loadContractors     =   formSchTask('updateContractors', 'Load all configuration info for agents from database', 0, None, {'onStart': True} ) 

#add(refreshServerStat)
#add(checkManageUpdate)
#add(loadContractors)
