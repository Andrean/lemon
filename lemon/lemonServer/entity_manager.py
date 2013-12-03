'''
Created on 20.08.2013

@author: vau
'''

import lemon
import core
import time
import uuid
import collections

COMMANDS    = collections.namedtuple('COMMANDS',['get_self_info'])
commands    = COMMANDS(get_self_info='get_self_info')
CMD_STATUS  = collections.namedtuple('CMD_STATUS',['present','submit','pending','completed','error'])
status      = CMD_STATUS(
                present   = 0,
                submit    = 1,
                pending   = 2,
                completed = 3,
                error     = -1
            )

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
        self.commandManager = CommandManager(self)
        self.fileManager    = FileManager()
        self._setReady()
        i = 0
        while(self._running):
            if i > 60:
                self.commandManager.clean()
                i = 0
            i+= 4                               
            self.update()
            time.sleep(4)
    
    def addNewAgent(self, agent_id):
        self.tagManager.assignTag(agent_id, agent_id)
        self.sendCommand(commands.get_self_info, [], [agent_id])
        
    def sendCommand(self, cmd, args, tags=[]):
        self.commandManager.addCommand(cmd, args, tags)
        self._logger.info('SEND command "{0}" to groups "{1}"'.format(cmd, str(tags)))        
        
    def getConfig(self, agent_id):
        tags    = self.tagManager.getTags(agent_id)
        return self.configManager.getConfig(tags)
    
    def getCommands(self, agent_id, timestamp=0):        
        tags    = [x for x in self.tagManager.getTags(agent_id)]        
        if len( tags ) > 0:
            return self.commandManager.getCommands(tags, timestamp)
        self._logger.info('Detected new agent with id {0}'.format(agent_id))
        self.addNewAgent(agent_id)
        return self.commandManager.getCommands([agent_id], 0)                
    
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
    """
        Command Manager has one list for commands and one hastable for status of execute commands on agents
        self._cmds, list of commands,  has next structure:
        [
        'id': string,
        'tags': [string], for which this command is applied
        'cmd': string , this is the text name of command
        'args': [string], text arguments for command
        'time': float,    time of creation of command
        ]
        self._cmds_status is dict of command execute statuses, key is command identificator
        Its structure:
        {
            command_id: [
                {
                    'agent_id':    string,
                    'status':    integer,
                    'time':    time
                }                
            ]        
        }
    """
    def __init__(self, manager):
        self.manager    = manager
        self._cmds   = []
        self._cmds_status   = {}    
        #self._st = core.getCoreInstance().getInstance('STORAGE').getInstance()
        #self._st.set_default_collection('commands')
        #for item in self._st.find({}):
        #    item['_id'] = None
        #    self._cmds.append(item)        
    
    def getCommands(self, tags, timestamp=0):
        result  = []        
        tags    = [x for x in tags]
        for cmd in self._cmds:            
            for tag in cmd['tags']:
                if tag in tags and cmd['time'] > timestamp:
                    result.append({'cmd': cmd['cmd'], 'args':cmd['args'], 'id':cmd['id']})
        return result
    
    def addCommand(self, cmd, args, tags):
        command_id = str(uuid.uuid4())
        self._cmds.append({ 
            'id': command_id,
            'tags': tags,
            'cmd': cmd,
            'args': args,
            'time': time.time()          
        })
        self._cmds_status[command_id]   = []
        self.manager._logger.debug('Added command {0}:  {1},{2},{3}'.format(command_id,str(cmd),str(args),str(tags)))                   
        
    def changeStatus(self, agent_id, command_id, status):
        try:
            self._cmds_status[command_id].append({'agent_id': agent_id, 'status': status, 'time': time.time()})
        except KeyError:
            self.manager._logger.error('Attempt to change status of not existing command {0} from agent {1} with status {3}'.format(str(command_id), str(agent_id), str(status)))
            return
    
    def _update(self):
        pass        
        #for cmd in self._st.find({}):
        #    self._st.save(cmd)
        #    cmd['_id'] = None
        #    self._cmds.append(cmd)
    def clean(self):
        self.manager._logger.debug('Calling cleaning commands')
        print(self._cmds)
        
        timestamp = time.time() - 60
        self._cmds[:] = [x for x in self._cmds if x['time'] > timestamp]
        print(self._cmds)  
                      
            
class FileManager(object):
    def __init__(self):
        self._st = core.getCoreInstance().getInstance('STORAGE').getInstance()
        self._st.set_default_collection('files')
            
    def getFile(self, file_id):
        self._st.set_default_collection('files')
        file    = self._st.findOne({'id': file_id})
        return {'name': file['filename'],'size': file['size'],'chunk':file['chunk']}
        
        