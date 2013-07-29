'''
    Created on 19.07.2013
    This module contains all standard tasks used in server
    @author: vau
'''

import json 
import time
import core

CMD = {}

def add(f):
    CMD[f.__name__] = f
    
@add
def storeAgentData(tm, dict_data):
    agent_data  = dict_data['agent']
    agent_id    = agent_data['__id']
    entity_id   = agent_id
    state       = agent_data['state']
    start_time  = agent_data['start_timestamp']
    st  = tm._storageManager.getInstance()
    st.set_default_collection(entity_id)
    query   = {'type': 'agent'}
    result  = [v for v in st.find(query)]
    doc_d   = {'type': 'agent', 'agent_id': agent_id,'state': state, 'start_time':start_time, 'end_time':None }
    
    if len(result) < 1:
        print(result)
        st.insert(doc_d)
    else:
        st.update(query, doc_d)
        
@add
def storeCurrentData(tm, dict_data):
    data        = dict_data['data']
    timestamp   = dict_data['time']
    entity_id   = dict_data['agent']['__id']
    st          = tm._storageManager.getInstance()
    st.set_default_collection(entity_id)
    q           =    {'type':'current'}
    item        = st.findOne(q)
    doc         = {'type':'current', 'data': data, 'time':timestamp}
    if item is None:
        st.insert(doc)
    else:
        st.update(q, doc)
    
@add
def storeData(tm, dict_data):
    agent       = dict_data['agent']
    data        = dict_data['data']
    timestamp   = dict_data['time']
    entity_id   = agent['__id']
    doc     = {'type': 'persistent', 'timestamp': timestamp, 'data': data}
    st      = tm._storageManager.getInstance()
    st.set_default_collection(entity_id)
    st.insert(doc)
    
@add
def refreshServerStat(tm, *args):
    print('REFRESH TEST')
    st  = tm._storageManager.getInstance()
    st.set_default_collection('server')
    c   = core.getCoreInstance()
    for name, inst in c._instances.items():
        q   = {'component': name}
        stat    = {}
        for k, v in inst.items():
            stat[k] = str(v)
        doc = {'component': name, 'stat': stat}
        st.update(q, doc)
    
@add
def updateContractors(tm, cfg):
    onStart = False
    try:
        if cfg['onStart']:
            onStart = True
    except KeyError:
        pass
    print('CHECKING DATABASE')
    st  = tm._storageManager.getInstance()
    st.set_default_collection('server')
    q   = {'type':'contractor'}
    c   = core.getCoreInstance()
    serverInstance  = c.getInstance('SERVER')
    cmdi    = serverInstance.cmdInterface
    for contractor in st.find(q):
        if onStart or contractor['modified']:
            contractor['modified'] = False
            st.update({'_id': contractor['_id']}, contractor)
            contractor['_id']   = None
            item    = {'__agents':'all', 'content': contractor}
            try:
                if contractor['deleted']:
                    cmdi.add(contractor['id'], 'del_contractor', item)                    
                    return
            except KeyError:
                pass
            cmdi.add(contractor['id'], 'add_contractor', item)
            
    
    q       = {'type': 'scheduled task'}
    for task in st.find(q):
        if onStart or task['modified']:
            print('FOUND TASK: ' + str(task))
            task['modified']    = False
            st.update({'_id': task['_id']}, task)
            task['_id'] = None
            item    = {'__agents':'all', 'content': task}
            try:
                if task['deleted']:
                    cmdi.add(task['id'], 'del_scheduled_task', item)
                    return
            except KeyError:
                pass
            cmdi.add(task['id'], 'add_scheduled_task', item)    
            
            
@add
def addScheduledTask(tm, dict_data):
    func_name       = dict_data['func']
    schtask_name    = dict_data['name']
    start_time      = dict_data['start_time']
    interval        = dict_data['interval']
    func_kwargs     = dict_data['kwargs']
    scheduler       = tm._scheduler
    if scheduler.getScheduledTask(schtask_name) is None:
        scheduler.add(func_name, schtask_name, start_time, interval, func_kwargs)
