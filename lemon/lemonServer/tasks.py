'''
    Created on 19.07.2013
    This module contains all standard tasks used in server
    @author: vau
'''

import json 

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
    data        = 'null'
    st  = tm._storageManager.getInstance()
    st.set_default_collection(entity_id)
    query   = {'type': 'current'}
    result  = [v for v in st.find(query)]
    doc_d   = {'type': 'current', 'agent_id': agent_id,'state': state, 'start_time':start_time, 'end_time':None, 'data': data }
    
    if len(result) < 1:
        print(result)
        st.insert(doc_d)
    else:
        st.update(query, doc_d)
    
    
@add
def addScheduledTask(tm, dict_data):
    pass
