#
#
#
#


def get_files( req, res ):
    try:
        #if not req.headers.__contains__('Lemon-Agent-ID'):
        #    raise KeyError
        #agent_id    = req.headers['Lemon-Agent-ID'] 
        #print(req.query['file'])
        files   = req.query.get('file', {})
        for f in files:
            print(f)
        res.send_content(str(files))
    except KeyError:
        res.send_error(401)
        return