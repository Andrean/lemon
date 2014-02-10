/**
 * 		/routes/system/agent/index.js
 * 
 * 		Load agent routes
 */

module.exports	= function( app ){
	var agent	= require('./controller.agent');
	
	app.get( '/agents',		agent.list		);
	app.post('/agents',		agent.modify	);
	app.get( '/agents/:id',	agent.show_one	);
};