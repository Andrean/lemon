
def get_commands( req, res ):
    res.send_response(200)
    res.send_header('Content-Type','text/plain;charset=utf-8')
    res.end_headers()
    res.send_content('This is command!')