
function init(){}

function groups_get(req, res) {
	res.render('groups')
}

exports.init	= init
exports.get		= groups_get