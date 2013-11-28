
def get_404( req, res ):
    res.send_response(404)
    res.send_content('Not found')