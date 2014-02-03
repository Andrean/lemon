/**
 * 		/controllers/system/index.js
 * 
 * 		Loader for all SYSTEM controllers 
 */

exports.get404	= function(req, res){
	if(req.accepts('html'))
		res.render('system_pages/404');
};
exports.get500	= function(req, res){};

exports.agent	= require('./agent');

exports.configuration	= require('./configuration');