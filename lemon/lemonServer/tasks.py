'''
    Created on 19.07.2013
    This module contains all standard tasks used in server
    @author: vau
'''

import json 
import time
import core


def getSchemaContractor():
    t    = { '__id': 'contractor_id', 
                            'name': 'getCPULoad',
                            'path': 'path_of_contractor',
                            'args': [],
                            'exit_code': 0,
                            'result': 'string',
                            'start_time': 0,
                            'duration_time': 0,
                            'state': 0                            
                           }
    return t

def getSchemaAgent():
    t         = {'agent_id': None,'state': None, 'start_time':0, 'end_time':None}
    return t

def getSchemaEntity():
    t        = {'entity_id': None, 'time': None, 'data': [getSchemaContractor()], 'agent': {}}
    return t

def getSchemaContractorData():
    t      = {'entity_id': None, 'time': None, 'data': [getSchemaContractor()]}
    return t

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
    st.set_default_collection('entities')
    query   = {'entity_id': entity_id}
    item    = st.findOne(query)
    if item is None:
        item    = getSchemaEntity()
    item['agent']   = {'agent_id': agent_id,'state': state, 'start_time':start_time, 'end_time':None }
    st.save(item)
    
    
        
@add
def storeCurrentData(tm, dict_data):
    data        = dict_data['data']
    timestamp   = dict_data['time']
    entity_id   = dict_data['agent']['__id']
    st          = tm._storageManager.getInstance()
    st.set_default_collection('entities')
    q           =    {'entity_id':entity_id}
    item        = st.findOne(q)
    if item is None:
        item    = getSchemaEntity()
        item['entity_id']   = entity_id       

    item['time']    = timestamp
    item['data']    = []
    for v in data.values():
        item['data'].append(v)
    st.save(item)

    
    
@add
def storeData(tm, dict_data):
    agent       = dict_data['agent']
    data        = dict_data['data']
    timestamp   = dict_data['time']
    entity_id   = agent['__id']
    st      = tm._storageManager.getInstance()
    st.set_default_collection('data')
    doc     = getSchemaContractorData()
    doc['entity_id']    = entity_id
    doc['time'] = timestamp
    doc['data'] = []
    for v in data.values():
        doc['data'].append(v)
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
