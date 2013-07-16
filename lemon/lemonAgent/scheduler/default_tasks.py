'''
Created on 16.07.2013

@author: vau
'''
def formSchTask(func, name, interval, start_time=None, kwargs={}):
    _task    = {'func': func,
                'name': name,
                'interval': interval,
                'start_time': start_time,
                'kwargs': kwargs
                }
    return _task

refreshServer       = formSchTask('refresh','refresh',5)
sendSelfInfoOnStart = formSchTask('sendSelfStat', 'Sending Self Information on start', 0)
sendSelfInfo        = formSchTask('sendSelfStat', 'Sending Self information by interval', 10)

tasks   = {}
tasks['refresh']    = refreshServer
tasks['sendSelfInfoOnStart']    = sendSelfInfoOnStart

