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

refreshServerStat  =   formSchTask('refreshServerStat', 'Refreshing server state and statistics', 10, None)

add(refreshServerStat)