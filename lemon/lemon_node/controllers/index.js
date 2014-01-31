/**
 * 		/controllers/index.js
 * 
 * 		Loader for all application controllers
 */
var mongoose	= require('mongoose')
	, Plugin	= mongoose.model('system.Plugin');

module.exports	= function( app, cb ){
	app.controllers	= {};
	app.controllers.system	= require('./system');	
	Plugin.find({enabled: true}, function(err, plugins){
		if(err){ console.log(err); return; }
		plugins.forEach( function( plugin ){
			app.controllers[plugin.name]	= require( './plugins/' + plugin.name );			
		});
		cb();
	});	
};