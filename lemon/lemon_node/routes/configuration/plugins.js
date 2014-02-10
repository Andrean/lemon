/**
 * 		/routes/configuration/plugins.js
 * 
 * 		Configuration routes for routes
 */

module.exports	= function( app, controller ){
	app.all( '/configuration/plugins', controller.load			);
	app.get( '/configuration/plugins/:name?', controller.show	);	
	app.put( '/configuration/plugins', 		  controller.add	);
	app.post('/configuration/plugins/:name?', controller.edit	);
};