'''
Created on 08.07.2013

@author: vau
'''

import time
import json
import lemon
import uuid
import os
import subprocess
from collections import namedtuple

MASK    = "contractor_layer"

_state   = namedtuple('STATE',['INIT','RUNNING','STOPPED'])

STATE   = _state(0, 1 , 2)

class Layer(lemon.BaseAgentLemon):
    '''
    This class is layer where stored info about subprocesses as contractors, used to read perfomance counters
    '''


    def __init__(self, _logger, _config, _storageInstance):
        '''
        Constructor
        '''
        self._storage   = _storageInstance
        self._contractors   = {}
        lemon.BaseAgentLemon.__init__(self, _logger, _config)
        self.contractors_path   = 'contractors/'
        try:
            self.contractors_path   = self._config['path']
        except KeyError:
            pass

        self._logger.info("Contractor layer initialized")
        
    def run(self):
        if not os.path.exists(self.contractors_path):
            os.makedirs(self.contractors_path)
        self._load()
        self._running   = True
        self._logger.info("Layer started")
        while self._running:
            time.sleep(0.01) 
        self._logger.info("Layer stopped")
        
    def addContractor(self, name, stream):
        c_id        = str(uuid.uuid4())
        contractor  = { 'name': name, 
                        '__id': c_id, 
                        'path': c_id + '.py', 
                        'state': STATE.INIT,
                        'args': [], 
                        'result': None, 
                        'exit_code': None }
        self._contractors[c_id] = contractor
        self._write(c_id + '.py', stream)
        self._store()
        
    def removeContractor(self, name):
        removed = None
        for k, v in self._contractors.items():
            if v['name'] == name:
                removed    = k
        self._contractors.pop(removed)
        self._store()
    
    def getStat(self):
        return self._contractors
    
    def startContractors(self, contractor_list):
        keys_contr  = []
        print(self._contractors)
        for key, v  in self._contractors.items():
            for k in contractor_list:
                if v['name'] == k:
                    keys_contr.append(key)
        for k in keys_contr:            
            path    = self._contractors[k]['path']
            args    = self._contractors[k]['args']
            self._start(k, path, args)
            self._logger.info('Started contractor {0} with id {1}'.format(self._contractors[k]['name'], self._contractors[k]['__id']))
    
    def stopContractors(self, contractor_list):
        for k in contractor_list:
            path    = self._contractors[k]['path']
            args    = self._contractors[k]['args']
            self._stop(path, args)
    
    def _start(self, k, path, args):
        c    = Contractor(self._logger, self._config, self._contractors[k], self.contractors_path + path, args)
        c.start()
    
    def _stop(self, k, path):
        pass
    
    def _write(self, path, content):
        try:
            path    = self.contractors_path + path
            f   = open(path,'w')
            f.write(content)
        except Exception as e:
            self._logger.exception(e)
        
    def _load(self):
        try:
            value   = self._storage.readStr(MASK)
            print(value)
            if value is not None:
                self._contractors   = json.loads(value)
        except Exception as e:
            self._logger.exception("Error occured in _load", e)
            
    def _store(self):
        try:
            content     = json.dumps(self._contractors)
            self._storage.writeItem(MASK, content)
        except Exception as e:
            self._logger.exception(e)
    
class Contractor(lemon.BaseAgentLemon):
    
    def __init__(self, _logger, _config, _place, path, args):
        self._place = _place
        self._call_args = [path]
        self._call_args.extend(args)
        lemon.BaseAgentLemon.__init__(self, _logger, _config)
        self._logger.info("contractor {0} created".format(self._place['__id']))
    
    def run(self):
        self.running    = True
        self.out    = ""
        self.err    = ""
        print(self._call_args)
        exit_code   = subprocess.call(["python.exe", self._call_args[0]])
        print('exit_code: {0}'.format(str(exit_code)))
        print('stdout: {0}\nstderr: {1} '.format(str(self.out), str(self.err)))