#
#    Структура плагина
#
#    экспортируемые методы:
#        get_commands()
#        get_version()
#

#    Plugin: Webpersonal
#    Version: 12
#

import importlib.machinery
import os

directory   = os.path.normpath(os.path.dirname(__file__))
loader      = importlib.machinery.SourceFileLoader( 'commands' , os.path.join(directory, 'commands.py') )
commands    = loader.load_module('commands')     

def get_commands():
    return commands.COMMANDS