/**
 * 	System controllers
 */

exports.get404	= function(req, res){
	if(req.accepts('html'))
		res.render('system_pages/404');
};
exports.get500	= function(req, res){};