/**
 * 		/routes/configuration/entities.js
 * 
 * 		Routes for configuration of entities
 */

module.exports	= function( app, controller ){
	app.param( 'entity_id',				controller.load );
	app.all( '/configuration/entities', controller.list			);
	app.get( '/configuration/entities/:entity_id?', controller.show	);	
	app.put( '/configuration/entities', 		  	controller.add	);
	app.post('/configuration/entities/:entity_id?', controller.edit	);
	app.del( '/configuration/entities/:entity_id' , controller.remove	);
};