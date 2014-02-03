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
exports.plugins.show	= function( req, res ){
	res.render('configuration/plugins', { title: 'Plugins', bg_color: 'bg-color-Dark'} );
};
//################################################################
