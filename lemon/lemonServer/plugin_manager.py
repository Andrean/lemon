'''
Created on 28 янв. 2014 г.
    
    Plugin Manager
    
    - manages plugins
    - manages its routes, commands, controllers

@author: Andrean
'''
import lemon
import time
import core
import sys
import importlib.machinery


class PluginManager(lemon.BaseServerComponent):
    '''
        Plugin:
        {
            name:      String,
            version:   Number,
            main:      ./plugins/name/plugin.py
            files:     [path/to/onefile]
            module:    Object - loaded plugin
            enabled:   Boolean
        }
    '''
    
    def __init__(self, _logger, _config, _info):
        lemon.BaseServerComponent.__init__(self, _logger, _config, _info)
        self.plugins    = []
        
    def run(self):
        self.load()        
        #self.add({'name':'webpersonal','version':12})        
        self._setReady()
        while self._running:
            time.sleep(0.1)
        self._logger.info('Shutdown plugin manager')
        
    def load(self, plugin_name=None):
        db  = core.getCoreInstance().getInstance('STORAGE').getInstance()
        db.set_default_collection('plugins')
        def __load_plugin(plugin):
            try:
                l   = importlib.machinery.SourceFileLoader('plugins.'+ plugin['name'], plugin['main'])
                plugin['module']   = l.load_module('plugins.' + plugin['name'])
                self._logger.info('Plugin "{0}" was loaded successfully'.format(plugin['name']))
            except:                        
                self._logger.error('Excepted error while loading plugin "{0}": {1}'.format(str(plugin['name']), sys.exc_info()[1]))
                raise
        if plugin_name:
            plugin  = db.findOne({'name': plugin_name})
            if not plugin:
                raise PluginNotFoundError('Plugin \"{0}\" not found'.format(plugin_name))
            for p in self.plugins:
                if p['name'] == plugin_name:
                    __load_plugin(p)                    
            return
        # loading all plugins    
        for plugin in db.find({}):
            plugin['module']    = None
            __load_plugin(plugin)            
            self.plugins.append(plugin)            
    
    def unload(self, plugin_name=None):
        pass
    
    def store(self):
        db  = core.getCoreInstance().getInstance('STORAGE').getInstance()
        db.set_default_collection('plugins')
        stack   = []
        for plugin in self.plugins:
            stack.append(plugin.pop('module'))            
            db.save(plugin)
            plugin['module'] = stack.pop()
    
    def add(self, new_plugin):
        self._logger.debug('Adding new plugin {0}'.format(new_plugin['name']))
        new_plugin['files'] = []
        new_plugin['module']= None
        new_plugin['main']  = './plugins/' + new_plugin['name'] + '/plugin.py'
        new_plugin['enabled'] = False
        def find():
            for k,v in enumerate(self.plugins):
                if v['name'] == new_plugin['name']:
                    return k
        plugin_i = find()
        if plugin_i is None:
            plugin  = new_plugin
            self.plugins.append(plugin)
        else:
            self._logger.debug('Plugin was found. Update it')
            _id = self.plugins[plugin_i]['_id']
            new_plugin['_id']   = _id
            self.plugins[plugin_i]  = new_plugin            
        self.store()   
    
    def getCommands(self):
        __commands  = {}
        for p in self.plugins:
            for v in p['module'].get_commands():
                __commands[v] = p['name'] + '.' + v
        return __commands
            #yield [(lambda cmd: p['name'] + '.' + cmd)(x) for x in ]
    
    def getRoutes(self, method, _filter):
        routes  = []
        for p in self.plugins:
            r = p['module'].get_routes(method, _filter)
            if r:
                routes.extend(r)
        return routes               
                 

class PluginNotFoundError(LookupError):
    pass