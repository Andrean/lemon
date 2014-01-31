/**
*	/routes/plugins/webpersonal/index.js
*
*	loader for routes of plugin 'Webpersonal'
*
*/

function load( app ){
	require('./main')( app );
}

module.exports	= load;