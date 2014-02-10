/**
*	/<routes>/webpersonal/main.js
*
*	main routes of plugin 'Webpersonal'
*/

module.exports	= function( app ){
	var wp	= require('./controllers');
	
	app.param('service'	, wp.loadServiceMap			);	// returns req.map
	app.all( '/webpersonal(/*)?', 	wp.loadSystems					);
	app.get( '/webpersonal',		wp.main_view					);	
	app.get( '/webpersonal/update/:service?'		, 		wp.view 		);
	app.post('/webpersonal/update/:service/upload'	, 		wp.upload 		);
	app.post('/webpersonal/update/:service/setup'	, 		wp.setup		);
	app.get( '/webpersonal/update/:service/status'	, 		wp.get_status	);
	app.post('/webpersonal/update/:service/switch_services',wp.switch_services	);
	app.post('/webpersonal/update/:service/switch_fronts', 	wp.switch_fronts	);
	app.get( '/webpersonal/configure/:service?'		, 		wp.configure		);
	app.post('/webpersonal/configure/:service/map'	, 		wp.edit_map			);
	app.del( '/webpersonal/configure/:service/map'	, 		wp.del_map			);
	app.post('/webpersonal/configure/:service/system', 		wp.edit_system_map	);
	app.get( '/webpersonal/configure/:service/services'	, 	wp.services			);
	app.post('/webpersonal/configure/:service/services'	, 	wp.edit_services	);
	app.put( '/webpersonal/projects/new',		wp.projects_new		);
	app.get( '/webpersonal/settings/pull',		wp.git_pull			);
	app.get( '/webpersonal/history/:service?',	wp.get_history		);
};