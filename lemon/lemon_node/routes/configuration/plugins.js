/**
 * 		/routes/configuration/plugins.js
 * 
 * 		Configuration routes for routes
 */

module.exports	= function( app ){
	var plugins_controller	= app.controllers.system.configuration.plugins;
	
	app.get( '/configuration/plugins/:name?', plugins_controller.show	);
};