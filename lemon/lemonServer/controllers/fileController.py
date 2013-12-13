#
#
#
#
import core
import entity_manager
import shutil
import os

def get_files( req, res ):
    try:
        em  = core.getCoreInstance().getInstance('ENTITY_MANAGER')
        files   = req.query.get('file', {})
        f = files[0]
        fd  = None
        try:
            fd, filename  = em.fileManager.getFileByLink(f) 
            fs = os.fstat(fd.fileno())            
            res.send_response(200)
            res.send_header('Content-Length', str(fs[6]))
            res.send_header('Content-Type','application/octet-stream')
            res.send_header('Content-Disposition','attachment; filename="{0}"'.format(filename))            
            res.end_headers()
            shutil.copyfileobj(fd, res.wfile)             
        except entity_manager.VirtualLinkNotExists:
            res.send_error(404)
        finally:
            if fd:
                fd.close()
    except KeyError:
        res.send_error(401)
        return