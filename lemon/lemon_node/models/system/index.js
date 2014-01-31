/**
 * 		/models/system/index.js
 * 
 * 		Loader for system models
 */

var mongoose 	= require('mongoose')
	, fs		= require('fs')
	, path		= require('path');

function load(){
	fs.readdirSync(__dirname).forEach( function(file){
		if( ~file.indexOf('.js') && file != path.basename(__filename))
			require( path.join( __dirname, file) )(path.basename(__dirname) + '.');
	});
}

module.exports	= load();