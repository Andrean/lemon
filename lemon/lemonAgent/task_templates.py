'''
Created on 09.07.2013
Task templates, which used to do some useful actions
@author: vau
'''
import json
import socket
import core


CMD = {}

def add(f):
    CMD[f.__name__] = f

@add
def runCounter(t, counter_id, kwargs):
    pass

@add
def addScheduledTask(t, kwargs):
    func_name       = kwargs['func']
    schtask_name    = kwargs['name']
    start_time      = kwargs['start_time']
    interval        = kwargs['interval']
    func_kwargs     = kwargs['kwargs']
    scheduler       = t._parent.scheduler
    if scheduler.getScheduledTask(schtask_name) is None:
        scheduler.add(func_name, schtask_name, start_time, interval, func_kwargs)
        
@add
def delScheduledTask(t, kwargs):
    scheduler       = t._parent.scheduler
    task_name       = kwargs['name']
    print('!!! DELETING SCHEDULER TASK {0}'.format(task_name))
    scheduler.remove(task_name)
    
@add   
def updateStat(t, kwargs):
    try:
        if kwargs['core']:
            core.getCoreInstance().updateStat()            
    except KeyError:
        pass
@add    
def sendSelfStat(t, kwargs):
    agentID = t._parent.agentID
    i       = t._parent.interfaceInstance
    cLayer  = t._parent.contractorLayer
    c_data  = cLayer.getStat()
    print('STATISTICS:   ' + str(c_data))
    info    = {'agent': {'__id': agentID, 'state': 'started'}}
    ip      = socket.gethostbyname(socket.gethostname())
    info['agent']['ip'] = ip
    info['data']    = {'contractors': c_data}
    i.post(info)
    
@add    
def getNewData(t, kwargs):
    i           = t._parent.interfaceInstance
    last_refresh    = kwargs['last_refresh']
    new_data    = i.get('new',last_refresh)
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
        agents  = item['__agents']
        timestamp   = item['__add_timestamp']
        cmd_type    = item['__type']
    except KeyError as e:
        print(e)
        return
    print('COMMAND: ' + command)
    
    if cmd_type == 'add_scheduled_task':
        schedulerInstance   = t._parent.scheduler
        if schedulerInstance.getScheduledTask(content['name']) is not None:
            print('task "{0}" exists'.format(content['name']))
        else:
            t._parent.new_task('addScheduledTask', content)    
    elif cmd_type == 'add_contractor':
        t._parent.new_task('addContractor', content)
    elif cmd_type == 'del_contractor':
        t._parent.new_task('delContractor', content)
    elif cmd_type == 'del_scheduled_task':
        t._parent.new_task('delScheduledTask', content) 
        
@add
def addContractor(t, kwargs):
    print('!!!!!!!!!!!!!!!!!!!!!!ADD CONTRACTOR: '+ str(kwargs))
    name    = kwargs['name']
    content = kwargs['content']
    cLayer  = t._parent.contractorLayer
    cLayer.addContractor(name, content)
    
@add
def delContractor(t, kwargs):
    print('!!!!!!!!!!!!!!!!!!!! DEL CONTRACTOR: '+ str(kwargs))
    name    = kwargs['name']
    cLayer  = t._parent.contractorLayer
    cLayer.removeContractor(name)

@add
def runContractor(t, kwargs):
    contractor  = kwargs['contractor']
    cLayer      = t._parent.contractorLayer
    cLayer.startContractors([contractor])
    
@add    
def refresh(t, kwargs):
    i           = t._parent.interfaceInstance
    i.get() 
       
@add    
def testPrint(t, kwargs):
    print(kwargs['los'])
    try:
        if kwargs['t']:
            print('i am task with id '+str(t.id))
    except KeyError:
        pass
