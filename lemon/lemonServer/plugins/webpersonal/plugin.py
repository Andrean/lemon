


import importlib.machinery
import os

NAME    = 'webpersonal'
VERSION = 12

Loader  = importlib.machinery.SourceFileLoader
commands    = Loader(NAME + '.commands', os.path.join(__file__,'..','commands.py')).load_module(NAME + '.commands')
routes      = Loader(NAME + '.routes'  , os.path.join(__file__,'..','routes.py'  )).load_module(NAME + '.routes'  )

def get_commands():
    return commands.get()

def get_routes(method,_filter=None):
    return routes.get(method, _filter)
