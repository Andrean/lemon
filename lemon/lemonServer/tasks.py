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
    print('i am storage data ' + str(dict_data))
    '''
    st  = tm._storageManager.getInstance()
    entity_id   = dict_data['agent']['__id']
    st.set_default_collection(entity_id)
    query   = "{'name': 'agent'}"
    doc  = "{'name': 'agent' , '__id': '{0}', 'data': {1} }".format(entity_id, json.dumps(dict_data))
    
    st.update(query, doc)
    '''
    
@add
def addScheduledTask(tm, dict_data):
    pass
