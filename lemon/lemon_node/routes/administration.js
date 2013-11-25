

function update( req, res ){
	var service = req.params.service
	console.log(service)
	res.render("administration/update",{'service': service})
}

exports.update = update