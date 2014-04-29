/**
 * 		/routes/configuration/agents.js
 */

module.exports	= function( app, controller ){
	app.param( 'agent_id',				controller.load );
	app.all( '/configuration/agents', controller.list			);
	app.get( '/configuration/agents/:agent_id?', controller.show	);	
	app.put( '/configuration/agents', 		  	 controller.add		);
	app.post('/configuration/agents/:agent_id?', controller.edit	);
	app.del( '/configuration/agents/:agent_id' , controller.remove	);
};