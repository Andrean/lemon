'''
Created on 21.08.2013

@author: vau
'''

import lemon
import core
import time

class EntityManager(lemon.BaseAgentLemon):
   
    def __init__(self, _logger, _config, _info):
        lemon.BaseAgentLemon.__init__(self, _logger, _config, _info)
        self.contractorList = {}
        self.scheduleList   = {}
        
    def run(self):
        self.contractorLayer    = core.getCoreInstance().getInstance('CONTRACTOR')
        self.scheduler          = core.getCoreInstance().getInstance('SCHEDULER')
        self.contractorList = self.contractorLayer.getContractors()
        self.scheduleList   = self.scheduler.getScheduledTask()
        self._setReady()
        while self._running:
            time.sleep(1)
            
    def getItem(self, _id=None,_name=None):
        if _id is not None:
            return self.getList()[_id]
        if _name is not None:
            for v in self.contractorList.values():
                if v['name'] == _name:
                    return v
            for v in self.scheduleList.values():
                if v['name'] == _name:
                    return v            
    
    def getList(self):
        l   = self.contractorList
        l.update(self.scheduleList)
        
    
    def updateList(self, cfg_list):
        try:
            for row in cfg_list:
                if row['__type'] == 'contractor':
                    add = True
                    for item in self.contractorList.values():
                        if item['name'] == row['content']['name']:
                            add = False 
                            if item['__revision'] < row['__revision']:
                                self.contractorLayer.removeContractor(item['name'])
                                self.contractorLayer.addContractor(item['name'], row['content']['content'], row['__revision'])                        
                    if add is True:
                        self.contractorLayer.addContractor(row['content']['name'], row['content']['content'], row['__revision'])
                if row['__type'] == 'scheduled_task':
                    add = True
                    for item in self.scheduleList.values():
                        if item['name'] == row['content']['name']:
                            add = False
                            if item['__revision'] < row['__revision']:
                                self.scheduler.remove(item['name'])
                                r   = row['content']
                                self.scheduler.add(r['func'],r['name'],r['start_time'],r['interval'],r['kwargs'],row['__revision'])
                    if add is True:
                        self.scheduler.add(r['func'],r['name'],r['start_time'],r['interval'],r['kwargs'],row['__revision'])
            for item in self.contractorList.values():
                remove = True
                for row in cfg_list:
                    if row['__type'] == 'contractor' and row['content']['name'] == item['name']:
                        remove = False
                if remove:
                    self.contractorLayer.removeContractor(item['name'])
            for item in self.scheduleList.values():
                if item['__revision'] < 0:
                    continue
                remove = True
                print(item['name'])                
                for row in cfg_list:
                    if row['__type'] == 'scheduled_task' and row['content']['name'] == item['name']:
                        remove = False
                if remove:
                    print('removing item: '+item['name'])
                    self.scheduler.remove(item['name'])
        except Exception as e:
            self._logger.exception(e)            
        self.contractorList = self.contractorLayer.getContractors()
        self.scheduleList   = self.scheduler.getScheduledTask()
        print(self.contractorList)
        print(self.scheduleList)
        