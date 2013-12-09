'''
Created on 20.08.2013

@author: vau
'''

import lemon
import core
import time
import uuid
import collections
import os

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
        self.agentManager   = {}
        
    def run(self):
        self.configManager  = Configuration()
        self.tagManager     = TagManager() 
        self.commandManager = CommandManager(self)
        self.fileManager    = FileManager('files')
        self.agentManager   = AgentManager()
        self.dataManager    = DataManager()
        self._setReady()
        i = 0
        while(self._running):
            if i > 60:
                self.commandManager.clean()
                i = 0
            i+= 4                               
            self.update()
            self.fileManager.removeOldLinks()
            time.sleep(4)
        self._logger.info('stop ENTITY_MANAGER')
    
    def addNewAgent(self, agent_id):
        self.agentManager.add(agent_id)
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
    
    def saveData(self, data):
        #self.dataManager.save()
        pass
    
    def update(self):
        pass
        #self.configManager._update()
        #self.tagManager._update()
        #self.commandManager._update()

class DataManager(object):
    def __init__(self):
        self._db    = core.getCoreInstance().getInstance('STORAGE').getInstance()    
    
class AgentManager(object):
    def __init__(self):
        self._agents    = core.getCoreInstance().getInstance('STORAGE').getInstance()
        self._agents.set_default_collection('agents')
        
    def add(self, agent_id):
        if len([x for x in self._agents.find({'agent_id': agent_id})]) > 0:
            pass
        agent   = {'agent_id': agent_id, 'tags': []}
        self._agents.save(agent)
        
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
    """
        Управляет коллекцией tags
        tags    = [
            {
                'tag': string , внутреннее название тэга,
                'name' : string, человекопонятное название,
                'description': описание тега
            }
        
        ]
    """
    def __init__(self):
        self._st_agents = core.getCoreInstance().getInstance('STORAGE').getInstance()
        self._st_agents.set_default_collection('agents')
        self._st_tags   = core.getCoreInstance().getInstance('STORAGE').getInstance()
        self._st_tags.set_default_collection('tags')
        
    def getTags(self, agent_id=None):
        """
            Return tags for agent_id. If agent_id is None then return all known tags
        """
        if agent_id is None:
            for x in self._st_tags.find({}):
                yield x
        tags   = [x for x in self._st_tags.find({})]
        for item in self._st_agents.find({'agent_id': agent_id}):
            for tag in item.get('tags',[]):     
                if tag in tags or tag == agent_id:               
                    yield tag                        
        
    def assignTag(self, agent_id, *tags):
        self._st_agents.update( 
            {'agent_id':agent_id }, 
            { "$addToSet": { 'tags': { "$each": tags } } }
        )
        
    def _update(self):
        pass
        #self._tagList   = []
        #self._st = core.getCoreInstance().getInstance('STORAGE').getInstance()
        #self._st.set_default_collection('groups')
        #for item in self._st.find({}):
        #    self._tagList.append(item)
  
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
        
    def clean(self):
        self.manager._logger.debug('Calling cleaning commands')
        print(self._cmds)
        
        timestamp = time.time() - 60
        self._cmds[:] = [x for x in self._cmds if x['time'] > timestamp]
        print(self._cmds)
            
class FileManager(object):
    def __init__(self, files_directory):
        self._root  = files_directory
        self._links = {}
        os.makedirs(self._root, exist_ok=True)
    
    def isExistsFile(self, filename):
        return os.path.exists(os.path.join(self._root, filename))
        
    def writeFile(self, filename, rstream, length):
        if filename is None: return
        path    = os.path.join(self._root, filename)
        with open(path, 'wb') as wstream:
            buf_length  = 40000
            while length > 0:
                write_len   = buf_length if length > buf_length else length
                buffer  = rstream.read( write_len )
                wstream.write(buffer)
                length -= buf_length
            wstream.close()
        return True
    
    def getFilePath(self , filename):
        if filename:
            return os.path.join(self._root, filename)
        return
                    
    def getFileByLink(self, link):
        try:        
            fileRecord   =  self._links.get(link,0)
            if fileRecord == 0:
                raise VirtualLinkNotExists()
            file    = fileRecord['file']
            with open(file, 'rb') as f:
                return f
        except KeyError:
            raise WrongLinkRecord()
        
    def createVirtualLink(self, file_path, ttl=3600):   # time of live of link is 3600 seconds
        link    = 'file_'+ str(uuid.uuid4())
        self._links[link]   = {'file': file_path, 'ttl': int(ttl), 'time': time.time()}
        return link
    
    def removeOldLinks(self):
        current_time   = time.time()
        for k in self._links.keys():
            if self._links[k]['time'] + self._links[k]['ttl'] < current_time:
                del(self._links[k])

### Exceptions
class VirtualLinkNotExists(Exception):
    pass

class WrongLinkRecord(Exception):
    pass
