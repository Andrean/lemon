/**
 * 		Models.Index file
 * 
 * 		/models/index.js
 * 
 * 		Load all database modules
 */

// load system modules, then with Plugin model load plugins models
var mongoose	= require('mongoose')
	, fs		= require('fs')
	, path		= require('path');

function load(cb){
	// load system modules
	require('./system');
	// and then from Plugin model getting request to mongodb
	var Plugin	= mongoose.model('system.Plugin');
	Plugin.find({enabled: true}, function(err, plugins){
		if( err ){ console.log(err); return; }
		plugins.forEach( function( plugin ){
			fs.readdirSync(path.join(__dirname, 'plugins', plugin.name)).forEach( function(file){
				if( ~file.indexOf('.js'))
					require(__dirname + '/plugins/' + plugin.name + '/' + file)( plugin.name + '.'); 
			});
		});
		cb();
	});
};
module.exports	= load;