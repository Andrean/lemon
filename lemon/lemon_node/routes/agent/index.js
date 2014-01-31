/**
 * 		/routes/system/agent/index.js
 * 
 * 		Load agent routes
 */

module.exports	= function( app ){
	var agent	= app.controllers.system.agent;
	
	app.get( '/agents',		agent.list		);
	app.post('/agents',		agent.modify	);
};