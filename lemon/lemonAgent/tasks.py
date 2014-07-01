



import core


CMD = {}

def add(f):
    CMD[f.__name__] = f
    
@add
def get_commands(t):
    em  = core.getCoreInstance().getInstance('ENTITY_MANAGER')
    em.commandHandler.get_commands()