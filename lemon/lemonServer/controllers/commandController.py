#
#
#
#
import core
import json
import time



def get_commands( req, res ):
    try:
        agent_id    = req.headers['Lemon-Agent-ID'] 
        agent_timestamp = req.headers.get('Lemon-Agent-Timestamp','0')      
        em          = core.getCoreInstance().getInstance('ENTITY_MANAGER')
        commands    = json.dumps(em.getCommands(agent_id, agent_timestamp))
        timestamp   = str(int(time.time()*1000000))        
        res.send_content(commands, {'Lemon-Server-Timestamp': timestamp})    
    except KeyError:
        res.send_content("[]")
        return
    except:
        raise
        res.send_content('')
        return
     
