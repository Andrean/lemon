'''
Created on 27 янв. 2014 г.

@author: Andrean
'''
#    Structure of plugin:
#
#    {
#        'name': String,
#        'version': Number,
#        'enabled': Boolean,
#        'files': [ path_to_file1, path_to_file2 ],
#        'main': './plugins/<name>/plugin.py',
#        'module': Object or None if not loaded
#    }

webpersonal_plugin  = {
                'name':'webpersonal',
                'version':12,
                'enabled': True,
                'files':[],
                'main': './plugins/webpersonal/plugin.py',
                'module': None
            }

import core
import json
import sys
import importlib.machinery

STORE_NAME   = 'plugins'

class PluginManager(object):
    
    def __init__(self, logger):
        self.plugins    = []
        self._logger    = logger
        
    def getPlugins(self):
        return [ {'name': x['name'], 'version':x['version']} for x in self.plugins ]
    
    def loadPlugins(self):
        storage  = core.getCoreInstance().getInstance('STORAGE')
        try:
            self.plugins    = json.loads(storage.readStr(STORE_NAME) or '[]')
        except Exception as e:
            self._logger.exception(e)
            self.plugins    = []        
        self.plugins.append(webpersonal_plugin)
        for plugin in self.plugins:
            self.load(plugin['name'])
            
    def load(self, plugin_name):
        try:
            for plugin in self.plugins:
                if plugin['name'] == plugin_name:
                    loader  = importlib.machinery.SourceFileLoader('plugins.' + plugin['name'],plugin['main'])
                    plugin['module']    = loader.load_module('plugins.' + plugin['name'])
        except:
            self._logger.error('Failed to load plugin {0}'.format(str(plugin_name)))
            self._logger.exception(sys.exc_info()[1])
        
    def unload(self, plugin_name=None):        
        for p in self.plugins:
            p['module'] = None
    
    def add(self, plugin):
        pass
    
    def remove(self, plugin):
        pass
    
    def enablePlugin(self, name=None):
        pass
    
    def disablePlugin(self, name=None):
        pass
    
    def _store(self):
        def clean(p):
            p['module'] = None
            return p
        storage  = core.getCoreInstance().getInstance('STORAGE')
        storage.writeItem(json.dumps([ clean(x) for x in self.plugins  ] ))
        
    
    
if __name__ == "__main__":
    pass
    #loader  = importlib.machinery.SourceFileLoader('plugin.name1','tmodule.py')
    #tmodule = loader.load_module('plugin.name1')
    #m   = tmodule.MMM()
    #m.print("test")
    #m.connect()