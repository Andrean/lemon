'''
Created on 09.07.2013
Task templates, which used to do some useful actions
@author: vau
'''
import json
import socket
import core

def runCounter(t, counter_id, kwargs):
    pass

def addScheduledTask(t, kwargs):
    func_name       = kwargs['func']
    schtask_name    = kwargs['name']
    start_time      = kwargs['start_time']
    interval        = kwargs['interval']
    func_kwargs     = kwargs['kwargs']
    scheduler       = t._parent.scheduler
    if scheduler.getScheduledTask(schtask_name) is None:
        scheduler.add(func_name, schtask_name, start_time, interval, func_kwargs)
    
def updateStat(t, kwargs):
    try:
        if kwargs['core']:
            core.getCoreInstance().updateStat()            
    except KeyError:
        pass
    
def sendSelfStat(t, kwargs):
    agentID = t._parent.agentID
    i       = t._parent.interfaceInstance
    info    = {'agent': {'__id': agentID, 'state': 'started'}}
    ip      = socket.gethostbyname(socket.gethostname())
    info['agent']['ip'] = ip
    i.post(info)
    
def getNewData(t, kwargs):
    i           = t._parent.interfaceInstance
    new_data    = i.get('new')
    print('Found new commands: '+str(new_data))
    for k in new_data:
        print(k)
        item = i.get(k)       
        __dispatcher(t, {'command': k, 'item': item})
        
def __dispatcher(t, kwargs):
    try:
        print(kwargs)
        command = kwargs['command']
        item = kwargs['item']
        content = item['content']
        agents  = item['agents']
        timestamp   = item['timestamp']
    except KeyError as e:
        print(e)
        return
    print(command)
    
    if command == 'add_scheduled_task':
        schedulerInstance   = t._parent.scheduler
        if schedulerInstance.getScheduledTask(content['name']) is not None:
            print('task "{0}" exists'.format(content['name']))
        else:
            t._parent.new_task('addScheduledTask', content)
        
    
def refresh(t, kwargs):
    i           = t._parent.interfaceInstance
    i.get()    
    
def testPrint(t, kwargs):
    print(kwargs['los'])
    try:
        if kwargs['t']:
            print('i am task with id '+str(t.id))
    except KeyError:
        pass
    

        
CMD = {}
CMD['runCounter']           = runCounter
CMD['testPrint']            = testPrint
CMD['addScheduledTask']     = addScheduledTask
CMD['getNewData']           = getNewData
CMD['refresh']              = refresh
CMD['sendSelfStat']         = sendSelfStat
CMD['updateStat']           = updateStat
