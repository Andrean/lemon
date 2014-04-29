/**
 * 		/routes/configuration/index.js
 * 
 * 		Loader for configuration routes
 */

module.exports	= function( app ){
	var controllers	= require('./controller.configuration.js');
	require('./plugins')( app, controllers.plugins );
	require('./entities')( app, controllers.entities );
	require('./agents')( app, controllers.agents );
};