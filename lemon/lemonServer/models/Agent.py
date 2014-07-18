'''
Created on 01 июля 2014 г.

@author: Andrean
'''
import models.base as base

class Agent(base.Base):
    '''
    Schema:
        agent_id:    String,
        name:        String,
        tags:     [  String  ],
        entities: [  dbref "Entities" ]
    '''    
    def __init__(self, dbref=None):
        self.__collection = "agents"
        self.__data = {
            'agent_id': None,
            'name':     "",
            'tags':     [],
            'entities': []
        }
        self.__dbref = dbref
        super().__init__(self.__dbref, self.__collection, self.__data)     