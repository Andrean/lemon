'''
    Created on 19.07.2013
    This module contains all standard tasks used in server
    @author: vau
'''

import json 

def storeAgentData(tm, dict_data):
    st  = tm._storageManager.getInstance()
    st.set_default_collection('entities')
    entity_id   = dict_data['agent']['__id']
    query   = "{'entity_id': '{0}'}".format(entity_id)
    doc  = "{'entity_id': {0} , 'data': {1} }".format(entity_id, json.dumps(dict_data))
    
    #st.update(query, doc)
    

def addScheduledTask(tm, dict_data):
    pass