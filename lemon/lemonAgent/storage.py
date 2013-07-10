'''
Created on 14.06.2013

@author: vau
'''

import sys
import os
import common.IdGenerator
import threading
import time
import lemon
from exception.lemonException import StorageNotCreatedException 


def synchronized(func):
    '''Synchronization method decorator.'''

    def new_function(self, *args, **kwargs):
        self._lock.acquire()
        try:
            return func(self, *args, **kwargs)
        finally:
            self._lock.release()
    return new_function

class Storage(lemon.BaseAgentLemon):
    '''
    Class using different files for every item
    '''
    def __init__(self, _logger, _config, preinitFile='.storage'):
        '''
        Constructor
        '''
        lemon.BaseAgentLemon.__init__(self, _logger, _config)
        self._lock  = threading.Lock()
        self._encoding  = 'utf-8'
        try:
            self._path  = self._config['data_path']
        except KeyError as k:
            self._logger.error("config error. Cannot create storage: {0}".format(str(k)))
            raise StorageNotCreatedException('Configuration error. One or more fields in config is None')
            
        self._storageID = self._read(self._path + preinitFile) or ''
        
        if  self._storageID is '':                                        
            self._storageID = common.IdGenerator.GenerateNewUniqueID();
            self._logger.info("storage create new ID")
            self._write(self._path + preinitFile, self._storageID)
        else:
            self._storageID = str(self._storageID, self._encoding)
        self._logger.info("storage created with Id " + self._storageID)
        
                 
    def run(self):
        self._running = True
        self._logger.info("storage {0} started".format(self._storageID))
        if not os.path.exists(self._config['data_path']):
            os.makedirs(self._config['data_path'])
        while(self._running):
            time.sleep(0.1)
        self._logger.info("shutdown storage {0}".format(self._storageID))
        
    # return byte content from file
    def readItem(self, item_id):
        fileName = self._getFilename(item_id);
        self._logger.debug('Read item {0}'.format(item_id))
        return self._read(fileName);
    
    def readStr(self, item_id):
        fileName = self._getFilename(item_id);
        self._logger.debug('Read str item {0}'.format(item_id))
        return str(self._read(fileName), self._encoding)
    
    # transform content to byte sequence and write it into file
    def writeItem(self, item_id, content):
        fileName = self._getFilename(item_id);
        self._logger.debug('Write item {0} with content {0}'.format(item_id, str(content)))
        return self._write(fileName, content);
    
    def appendToItem(self, item_id, content):
        fileName = self._getFilename(item_id);
        return self._append(fileName, content);
    
    def deleteItem(self, item_id):
        fileName = self._getFilename(item_id);
        return self._delete(fileName)
    
    def quit(self):
        self._running = False
    
    @synchronized
    def _read(self, file):
        try:
            f = open(file, 'rb');
            content = f.read()
            f.close()
            return content
        except IOError:
            self._logger.info("{0} is not exists. Creating new file".format(str(file)));
        except Exception as ex:
            tb  = sys.exc_info()[2]
            self._logger.error(ex.with_traceback(tb))
        
    @synchronized              
    def _write(self, file, content):
        try:
            f = open(file, 'wb')
            f.write(bytes(content, self._encoding))
            return True
        except Exception as ex:
            tb = sys.exc_info()[2]
            self._logger.error(ex.with_traceback(tb))
        finally:
            f.close()
    
    @synchronized    
    def _append(self, file, content):
        try:
            f = open(file, 'ab+')
            f.write(bytes(content, self._encoding))
            return True
        except Exception as ex:
            tb = sys.exc_info()[2]
            self._logger.error(ex.with_traceback(tb))
        finally:
            f.close()
            
    @synchronized
    def _delete(self, file):
        try:
            os.remove(file)
            self._logger.debug("file {0} deleted".format(file))
            return True
        except Exception as e:
            tb = sys.exc_info()[2]
            self._logger.error(e.with_traceback(tb))
                
    def _getFilename(self, item_id):
        return self._path + '/' + self._storageID + str(item_id);
    