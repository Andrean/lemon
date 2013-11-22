var path	= 'system_pages/'

function get404(req, res){
	if(req.accepts('html'))
		res.render(path+'404')
}
function get500(req, res){}

exports.get404		= get404
exports.get500		= get500


