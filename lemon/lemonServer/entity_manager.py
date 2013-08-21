'''
Created on 20.08.2013

@author: vau
'''

import lemon
import core
import time

class EntityManager(lemon.BaseServerComponent):
    
    def __init__(self, _logger, _config, _info):
        lemon.BaseServerComponent.__init__(self, _logger, _config, _info)
        self.configManager  = {} 
        self.tagManager     = {}
        
    def run(self):
        self.configManager  = Configuration()
        self.tagManager     = TagManager() 
        self._setReady()
        while(self._running):
            self.update()
            time.sleep(1)
            
    def getConfig(self, agent_id):
        tags    = self.tagManager.getTags(agent_id)
        return self.configManager.getConfig(tags)
    
    def update(self):
        self.configManager._update()
        self.tagManager._update()



class Configuration(object):
    def __init__(self):
        self._revision      = 0
        self._config        = {}
        self._update()        
    
    def _update(self):
        stManager   = core.getCoreInstance().getInstance('STORAGE')
        st          = stManager.getInstance()
        st.set_default_collection('configuration')
        for item in st.find({}):
            if item['__type'] == 'revision':
                self.setRevision(item['content']['revision'])
                continue
            self._config[item['__id']] = item
            
    def setRevision(self, new_revision):
        self._revision = new_revision
        
    def getRevision(self):
        return self._revision
    
    def getConfig(self, tags):
        for item in self._config.values():
            for k in  item['__tags']:
                if k in tags:
                    item['_id'] = None
                    yield item 
            
class TagManager(object):
    def __init__(self):
        self._tagList   = []
        self._st = core.getCoreInstance().getInstance('STORAGE').getInstance()
        self._st.set_default_collection('groups')
        for item in self._st.find({}):
            self._tagList.append(item)
        
    def getTags(self, agent_id):
        for item in self._tagList:
            if item['agent_id'] == agent_id:
                yield item['tag']
        self.assignTag(agent_id, 'default')
        
    def assignTag(self, agent_id, _tag):
        t   = {'agent_id' : agent_id, 'tag': _tag}
        self._tagList.append(t)
        self._st.set_default_collection('groups')
        self._st.save(t)    
        
    def _update(self):
        self._tagList   = []
        self._st = core.getCoreInstance().getInstance('STORAGE').getInstance()
        self._st.set_default_collection('groups')
        for item in self._st.find({}):
            self._tagList.append(item)
  
        