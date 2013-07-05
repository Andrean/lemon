'''
Created on 05.07.2013

@author: vau
'''

import threading
import re
import pymongo
import time

class Storage(threading.Thread):
    
    def __init__(self, _logger, _cfg):
        '''
        Constructor
        '''
        self._logger    = _logger
        self._config    = _cfg
        self._collection    = ""
        self._running   = False
        
        mongodb_addr    = 'localhost';
        mongodb_port    = 27017;
        db_name         = 'mydb';
        try:
            self._client    = pymongo.MongoClient(mongodb_addr, mongodb_port)
            self._logger.info("Connection to mongodb successfully established")
            self._db = self._client[db_name]
            self._logger.debug("Successfully connected to '{0}'".format(db_name))
            self._running = True
            self._test  = 1
        except pymongo.errors.ConnectionFailure as err:
            self._logger.error("Cannot establish connection to database on {0}:{1}: {2}".format(mongodb_addr, mongodb_port, err));
        except KeyError:
            self._logger.error("Database '{0}' is not exists".format(db_name));
            exit(1);
        except Exception as err:
            self._logger.error("An exception raised during connection to database: {0}".format(err));
            exit(1);

        threading.Thread.__init__(self)
        
        
    def run(self):
        while(self._running):
            time.sleep(0.5)
            
    def quit(self):
        self._running = False
    
    def set_default_collection(self, collection_name):
        self._collection = collection_name
        
    def insert(self, doc, collection = None ):
        if collection is None:
            collection  = self._collection
        try:
            return self._db[collection].insert(doc)
        except pymongo.errors.DuplicateKeyError:
            self._logger.error("An duplicate key error raised on insert doc {0} to collection {1}".format(doc, collection));
    
    def update(self, query, doc, collection = None):
        if collection is None:
            collection  = self._collection
        try:
            return self._db[collection].update(query, doc)
        except pymongo.errors.PyMongoError as err:
            self._logger.error("PyMongoError raised on update doc {0} in collection {1}: {2}".format(str(doc), str(collection), str(err)))
    
    def remove(self, query, collection = None):
        if collection is None:
            collection  = self._collection
        try:
            return self._db[collection].remove(query)
        except pymongo.errors.PyMongoError as err:
            self._logger.error("PyMongoError raised on remove by query {0} in collection {1}: {2}".format(str(query), str(collection), str(err)))
    
    def find(self, query, collection = None):
        if collection is None:
            collection  = self._collection
        try:
            return self._db[collection].find(query)
        except pymongo.errors.PyMongoError as err:
            self._logger.error("PyMongoError was excepted during find by query {0}: {1}".format(str(query), str(err)))
        except KeyError:
            self._logger.error("Collection '{0}' is not found".format(str(collection)))
    
    def findOne(self, query, collection = None):
        if collection is None:
            collection  = self._collection
        try:
            return self._db[collection].find_one(query)
        except pymongo.errors.PyMongoError as err:
            self._logger.error("PyMongoError was excepted during find_one by query {0}: {1}".format(str(query), str(err)))
    
    def getCollections(self, query='.*'):
        try:
            print(self._db)
            colls = self._db.collection_names()
            return [x for x in colls if re.match(query, x) ]
        except pymongo.errors.PyMongoError as err:
            self._logger.error("PyMongoError was excepted during getting collections: {0}".format(str(err)))
    
    def createCollection(self, collection_name):
        try:
            self._db.create_collection(collection_name)
        except pymongo.errors.PyMongoError as err:
            self._logger.error("PyMongoError was excepted during creating collection {0}: {1}".format(str(collection_name), str(err)))
    
    
            
     