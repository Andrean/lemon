'''
Created on 05.07.2013

@author: vau
'''

import re
import pymongo
import time
import exception.lemonException
import lemon


def updateTimer(f):
    def wrapper(self, *args, **kwargs):
        self._info['last_used_time']    = time.time()
        return f(self, *args, **kwargs)
    return wrapper

class Storage(lemon.BaseServerComponent):
    
    def __init__(self, _logger, _config, _info):
        
        lemon.BaseServerComponent.__init__(self, _logger, _config, _info)
        self._collection    = ""
        mongodb_addr    = self._config['database'].get('host','localhost');
        mongodb_port    = self._config['database'].get('port',27017);
        db_name         = self._config['database'].get('db_name','lemon');
        try:
            self._client    = pymongo.MongoClient(mongodb_addr, mongodb_port)
            self._logger.info("Connection to mongodb successfully established")
            self._db = self._client[db_name]
            self._logger.debug("Successfully connected to '{0}'".format(db_name))
            self._test  = 1
        except pymongo.errors.ConnectionFailure as err:
            self._logger.error("Cannot establish connection to database on {0}:{1}: {2}".format(mongodb_addr, mongodb_port, err));
            raise exception.lemonException.StorageNotCreatedException("Cannot create storage")
        except KeyError:
            self._logger.error("Database '{0}' is not exists".format(db_name));
            exit(1);
            
        self._cmd           = {
                               'update':    self.update,
                               'insert':    self.insert,
                               'save':      self.save,
                               'remove':    self.remove,
                               'set_default_collection':    self.set_default_collection,
                               'find':      self.find,
                               'findOne':   self.findOne
                               }            
        
    @updateTimer
    def run(self):
        self._setReady()
        while(self._running):
            time.sleep(0.5)
        self._client.close()
        self._logger.info('Stop STORAGE {0} instance'.format(self._info['id']))
            
    def do(self, method, *args):
        #print('Requesting method {0} with args {1}'.format(method,str(args)))
        res = self._cmd[method](*args)
        #print("RESULT::::"+str(res))
        return res
    
    @updateTimer        
    def set_default_collection(self, collection_name):
        self._collection = collection_name
    
    @updateTimer    
    def insert(self, doc, collection = None ):
        if collection is None:
            collection  = self._collection
        try:
            return self._db[collection].insert(doc)
        except pymongo.errors.DuplicateKeyError:
            self._logger.error("An duplicate key error raised on insert doc {0} to collection {1}".format(doc, collection));
    
    @updateTimer
    def update(self, query, doc, collection = None):
        if collection is None:
            collection  = self._collection
        try:
            item    = self.findOne(query, collection)
            if item is None:
                return self.insert(doc,collection)
            return self._db[collection].update(query, doc)
        except pymongo.errors.PyMongoError as err:
            self._logger.error("PyMongoError raised on update doc {0} in collection {1}: {2}".format(str(doc), str(collection), str(err)))
    
    @updateTimer
    def save(self, to_save, collection = None):
        if collection is None:
            collection  = self._collection
        try:
            return self._db[collection].save(to_save, manipulate=False)
        except pymongo.errors.PyMongoError as err:
            self._logger.exception(err)
            
    @updateTimer
    def remove(self, query, collection = None):
        if collection is None:
            collection  = self._collection
        try:
            return self._db[collection].remove(query)
        except pymongo.errors.PyMongoError as err:
            self._logger.error("PyMongoError raised on remove by query {0} in collection {1}: {2}".format(str(query), str(collection), str(err)))
    
    @updateTimer
    def find(self, query, collection = None):
        if collection is None:
            collection  = self._collection
        try:
            return self._db[collection].find(query)
        except pymongo.errors.PyMongoError as err:
            self._logger.error("PyMongoError was excepted during find by query {0}: {1}".format(str(query), str(err)))
        except KeyError:
            self._logger.error("Collection '{0}' is not found".format(str(collection)))
    
    @updateTimer
    def findOne(self, query, collection = None):
        
        if collection is None:
            collection  = self._collection
        try:
            return self._db[collection].find_one(query)
        except pymongo.errors.PyMongoError as err:
            self._logger.error("PyMongoError was excepted during find_one by query {0}: {1}".format(str(query), str(err)))
    
    @updateTimer
    def getCollections(self, query='.*'):
        try:
            print(self._db)
            colls = self._db.collection_names()
            return [x for x in colls if re.match(query, x) ]
        except pymongo.errors.PyMongoError as err:
            self._logger.error("PyMongoError was excepted during getting collections: {0}".format(str(err)))
    
    @updateTimer
    def createCollection(self, collection_name):
        try:
            self._db.create_collection(collection_name)
        except pymongo.errors.PyMongoError as err:
            self._logger.error("PyMongoError was excepted during creating collection {0}: {1}".format(str(collection_name), str(err)))