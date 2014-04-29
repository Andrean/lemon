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

//////////////////////////////////////////////////////////////////
//ENTITIES CONTROLLERS
//////////////////////////////////////////////////////////////////
var  Entity	= mongoose.model('inventory.Entity');	
exports.entities	= {};
exports.entities.load		= function(req, res, next){
	Entity.load( req.params.entity_id, function(err, entity){
		if(err) throw err;
		res.entity	= entity;
	});
};
exports.entities.list		= function(req, res){
	Entity.list(function(err,entities){
		if(err) throw err;
		if(req.xhr)
			res.send(entities);
		else
			res.render('configuration/entities', {title: 'Configuration > Entities',  bg_color: 'bg-color-Dark', entities: entities });
	});
};
exports.entities.show		= function(req, res){};
exports.entities.add		= function(req, res){};
exports.entities.edit		= function(req, res){};
exports.entities.remove		= function(req, res){};
//################################################################
