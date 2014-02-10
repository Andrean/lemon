/**
 * 		/routes/index.js
 * 
 * 		Loader for all application routes
 */
var mongoose	= require('mongoose')
	, async		= require('async')
	, Plugin	= mongoose.model('system.Plugin')
	, system	= require('./controllers');

module.exports	= function( app ){
	
	app.get('/', function( req, res ){	res.redirect('/webpersonal'); });
	//////////////////////////////////////////////////////////////////////
	//	Loading all routes
	//////////////////////////////////////////////////////////////////////
	async.series([
	     function(cb){
    		require('./system')( app );
    		cb();
	     },
	     function(cb){
	    	require('./agent')( app );
	    	cb();	
	     },
	     function(cb){
	    	 require('./configuration')(app);
	    	 cb();
	     },
	     function(cb){
	    	Plugin.find({ enabled: true }, function(err, plugins){
    			if( err ){ console.log(err); return; }
    			plugins.forEach( function( plugin ){
    				require('./plugins/' + plugin.name)( app );
    			});
    			cb();
	    	});
	     }
	],
	function( err, _ ){
		//////////////////////////////////////////////////////////////////////
		app.all('*', system.get404);	
	});	
};