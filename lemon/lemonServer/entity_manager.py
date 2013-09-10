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
        self.commandManager = {}
        self.fileManager    = {}
        
    def run(self):
        self.configManager  = Configuration()
        self.tagManager     = TagManager() 
        self.commandManager     = CommandManager()
        self.fileManager    = FileManager()
        self._setReady()
        while(self._running):
            self.update()
            time.sleep(1)
            
    def getConfig(self, agent_id):
        tags    = self.tagManager.getTags(agent_id)
        return self.configManager.getConfig(tags)
    
    def getCommands(self, agent_id):
        tags    = self.tagManager.getTags(agent_id)
        return self.commandManager.getCommands(tags)
    
    def getFile(self, agent_id, file_id):
        return self.fileManager.getFile(file_id)
    
    def update(self):
        self.configManager._update()
        self.tagManager._update()
        self.commandManager._update()



class Configuration(object):
    def __init__(self):
        self._revision      = 0
        self._config        = []
        self._update()        
    
    def _update(self):
        stManager   = core.getCoreInstance().getInstance('STORAGE')
        st          = stManager.getInstance()
        st.set_default_collection('configuration')
        self._config = []
        for item in st.find({}):
            if item['__type'] == 'revision':
                self.setRevision(item['__revision'])
                continue
            try:
                if item['__enabled'] is False:
                    continue
            except KeyError:
                continue
            self._config.append(item)
            
    def setRevision(self, new_revision):
        self._revision = new_revision
        
    def getRevision(self):
        print("revision: "+str(self._revision))
        return self._revision
    
    def getConfig(self, tags):
        for item in self._config:
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
        if(len([x for x in self._st.find(t)]) > 0):
            pass
        else:
            self._tagList.append(t)
            self._st.set_default_collection('groups')
            self._st.save(t)    
        
    def _update(self):
        self._tagList   = []
        self._st = core.getCoreInstance().getInstance('STORAGE').getInstance()
        self._st.set_default_collection('groups')
        for item in self._st.find({}):
            self._tagList.append(item)
  
class CommandManager(object):
    def __init__(self):
        self._cmd   = []
        self._st = core.getCoreInstance().getInstance('STORAGE').getInstance()
        self._st.set_default_collection('commands')
        for item in self._st.find({'_new': True}):
            self._cmd.append(item)        
    
    def getCommands(self, tags):
        result  = {}        
        for _c in self._cmd:
            for tag in _c['tags']:
                if tag in tags:
                    result[_c['type']] = _c['arg']
        return result
            
        
    def _update(self):
        self._cmd   = []
        self._st = core.getCoreInstance().getInstance('STORAGE').getInstance()
        self._st.set_default_collection('commands')
        for cmd in self._st.find({'_new': True}):
            cmd['_new']  = False
            self._st.save(cmd)
            cmd['_new'] = None
            cmd['_id'] = None
            self._cmd.append(cmd)
            
class FileManager(object):
    def __init__(self):
        self._st = core.getCoreInstance().getInstance('STORAGE').getInstance()
        self._st.set_default_collection('files')
            
    def getFile(self, file_id):
        self._st.set_default_collection('files')
        file    = self._st.findOne({'id': file_id})
        return {'name': file['filename'],'size': file['size'],'chunk':file['chunk']}
        
        