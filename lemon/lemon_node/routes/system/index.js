/**
 * 		Load system routes
 */

module.exports	= function( app ){
	var controller	= require('./controller.system');
	
	app.get( '/lemon/commands/status', controller.lemon.get_status);
};