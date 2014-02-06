/**
 * 		/routes/configuration/plugins.js
 * 
 * 		Configuration routes for routes
 */

module.exports	= function( app ){
	var plugins_controller	= app.controllers.system.configuration.plugins;
	
	app.all( '/configuration/plugins', plugins_controller.load			);
	app.get( '/configuration/plugins/:name?', plugins_controller.show	);	
	app.put( '/configuration/plugins', 		  plugins_controller.add	);
	app.post('/configuration/plugins/:name?', plugins_controller.edit	);
};