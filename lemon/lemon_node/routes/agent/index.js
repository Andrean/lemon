/**
 * 		/routes/system/agent/index.js
 * 
 * 		Load agent routes
 */

module.exports	= function( app ){
	var agent	= require('./controller.agent');
	
	app.get( '/agents',		agent.list		);
	app.post('/agents',		agent.modify	);
	app.param( 'id', 		agent.load_agent);
	app.get( '/agents/:id',	agent.show_one	);
	app.get( '/agents/:id/update', agent.show_update	);
	app.put( '/agents/:id/update', agent.accept_update	);
	app.post('/agents/:id/update', agent.install_update	);
};