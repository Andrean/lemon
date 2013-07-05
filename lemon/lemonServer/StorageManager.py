'''
Created on 21.06.2013

@author: vau
'''

import pymongo
import threading
import re

class StorageManager(threading.Thread):
    
    def __init__(self, logger, cfg):
        '''
        Constructor
        '''
        self._masterST  = []
        self._logger    = logger
        self._config    = cfg       
        threading.Thread.__init__(self)
    
    def run(self):
        mongodb_addr    = 'localhost';
        mongodb_port    = 27017;
        db_name         = 'mydb';
        try:
            self._client    = pymongo.MongoClient(mongodb_addr, mongodb_port)
            self._logger.info("Connection to mongodb successfully established");
            self._db = self._client[db_name];
            self._logger.debug("Successfully connected to '{0}'".format(db_name));
        
        except pymongo.errors.ConnectionFailure as err:
            self._logger.error("Cannot establish connection to database on {0}:{1}: {2}".format(mongodb_addr, mongodb_port, err));
        except KeyError:
            self._logger.error("Database '{0}' is not exists".format(db_name));
            exit(1);
        except Exception as err:
            self._logger.error("An exception raised during connection to database: {0}".format(err));
            exit(1);
                
        
    
    def getInstance(self, _instanceName):
        return self._instance[_instanceName]
      
    def insert(self, collection, doc):
        try:
            return self._db[collection].insert(doc)
        except pymongo.errors.DuplicateKeyError:
            self._logger.error("An duplicate key error raised on insert doc {0} to collection {1}".format(doc, collection));
    
    def update(self, collection, query, doc):
        try:
            return self._db[collection].update(query, doc)
        except pymongo.errors.PyMongoError as err:
            self._logger.error("PyMongoError raised on update doc {0} in collection {1}: {2}".format(str(doc), str(collection), str(err)))
    
    def remove(self, collection, query):
        try:
            return self._db[collection].remove(query)
        except pymongo.errors.PyMongoError as err:
            self._logger.error("PyMongoError raised on remove by query {0} in collection {1}: {2}".format(str(query), str(collection), str(err)))
    
    def find(self, collection, query):
        try:
            return self._db[collection].find(query)
        except pymongo.errors.PyMongoError as err:
            self._logger.error("PyMongoError was excepted during find by query {0}: {1}".format(str(query), str(err)))
    
    def findOne(self, collection, query):
        try:
            return self._db[collection].find_one(query)
        except pymongo.errors.PyMongoError as err:
            self._logger.error("PyMongoError was excepted during find_one by query {0}: {1}".format(str(query), str(err)))
    
    def getCollections(self, query):
        try:
            colls = self._db.collection_names()
            return [x for x in colls if re.match(query, x) ]
        except pymongo.errors.PyMongoError as err:
            self._logger.error("PyMongoError was excepted during getting collections: {0}".format(str(err)))
    
    def createCollection(self, name):
        try:
            self._db.create_collection(name)
        except pymongo.errors.PyMongoError as err:
            self._logger.error("PyMongoError was excepted during creating collection {0}: {1}".format(str(name), str(err)))
    
    
            
    