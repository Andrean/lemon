/**
 * 		/controllers/system/configuration.js
 * 
 * 		Load all configuration controllers 
 */
var mongoose	= require('mongoose');

//////////////////////////////////////////////////////////////////
//	PLUGINS CONTROLLERS
//////////////////////////////////////////////////////////////////
var Plugin	=	mongoose.model('system.Plugin');  
exports.plugins	= {};
exports.plugins.load	= function( req, res, next ){
	Plugin.find({}, function( err, plugins ){
		if(err){ console.log('Error while loading plugins: '+err); res.send(500);}
		res.plugins	= plugins;
		next();
	});
};
exports.plugins.show	= function( req, res ){
	if( req.params.name )
		;
	else
		res.render('configuration/plugins', { title: 'Plugins', bg_color: 'bg-color-Dark', plugins: res.plugins} );		
};
exports.plugins.add		= function( req, res){};
exports.plugins.edit		= function( req, res){};

//################################################################