#
#
#
#
import core
import json
import time
import re
import entity_manager

def put_data( req, res):
    try:
        if not req.headers.__contains__('Lemon-Agent-ID'):
                raise KeyError
        agent_id        = req.headers['Lemon-Agent-ID']
        content_type    = req.headers.get('Content-Type','text/plain;charset=utf-8')
        content_length  = int(req.headers.get('Content-Length',0))
        if content_length == 0:
            res.send_error(411)
            return      
        charset         = 'utf-8'
        match = re.match(r';charset=([\w-]+)',content_type)
        if match:   
            charset = match.groups[1]
        body    = json.loads(str(req.rfile.read(content_length), charset))
        em      = core.getCoreInstance().getInstance('ENTITY_MANAGER')
        em.saveData(body)
        res.send_content('')
    except KeyError:
        res.send_error(401)

def post_agent_state( req, res ):
    pass