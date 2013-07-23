'''
    Created on 19.07.2013
    This module contains all standard tasks used in server
    @author: vau
'''

import json 
import time

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
def addScheduledTask(tm, dict_data):
    func_name       = dict_data['func']
    schtask_name    = dict_data['name']
    start_time      = dict_data['start_time']
    interval        = dict_data['interval']
    func_kwargs     = dict_data['kwargs']
    scheduler       = tm._scheduler
    if scheduler.getScheduledTask(schtask_name) is None:
        scheduler.add(func_name, schtask_name, start_time, interval, func_kwargs)
