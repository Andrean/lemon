#
#
#
#
import core
import json
import time
import re
import entity_manager


def get_commands( req, res ):
    try:
        if not req.headers.__contains__('Lemon-Agent-ID'):
            raise KeyError
        agent_id    = req.headers['Lemon-Agent-ID'] 
        agent_timestamp = req.headers.get('Lemon-Agent-Timestamp','0')      
        em          = core.getCoreInstance().getInstance('ENTITY_MANAGER')
        commands    = em.getCommands(agent_id, float(agent_timestamp),req.client_address)
        s_commands  = json.dumps(commands)
        timestamp   = str(time.time())       
        res.send_content(s_commands, {'Lemon-Server-Timestamp': timestamp})
        for k in commands:
            em.commandManager.changeStatus( agent_id, k['id'], entity_manager.status.submit )    
    except KeyError:
        res.send_error(401)
        return
    except:
        raise        
    
def post_commands_result( req, res ):
    try:
        if not req.headers.__contains__('Lemon-Agent-ID'):
            raise KeyError
        agent_id        = req.headers['Lemon-Agent-ID']
        agent_timestamp = req.headers.get('Lemon-Agent-Timestamp','0')
        content_type    = req.headers.get('Content-Type','text/plain;charset=utf-8')
        content_length  = int(req.headers.get('Content-Length',0))
        if content_length == 0:
            res.send_error(411)
            return      
        charset         = 'utf-8'
        match = re.match(r';charset=([\w-]+)',content_type)
        if match:   
            charset = match.groups[1]
        body_params    = json.loads(str(req.rfile.read(content_length), charset))
        em          = core.getCoreInstance().getInstance('ENTITY_MANAGER')
        for cmd in body_params:
            em.commandManager.changeStatus(agent_id, cmd['cmd_id'], cmd['status'], cmd['msg'])
        res.send_content('') 
    except KeyError:
        res.send_error(401)
        return
         
