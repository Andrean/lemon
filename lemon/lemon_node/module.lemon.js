/**
 * 	Module with Lemon functions
 */

var http	= require('http')
	, fs	= require('fs');

var lemon	= {};
//////////////////////////////////////////////////////////////////
// connect to lemon server
exports.connect	= function( _config, callback ){
	lemon	= _config;
	lemon.connected	= true;
	if(callback)
		callback(null);
};
//////////////////////////////////////////////////////////////////
// request prototype
exports.request	= function( method, path, headers, data, cb ){
	var options	= {
		hostname: lemon.server.hostname,
		port:	  lemon.server.port,
		path: 	  path,
		method:   method,
		headers:  headers
	};
	req	= http.request(options, function(res){
		if( res.statusCode == 200 || res.statusCode == 201 ){
			var data	= '';
			res.on('data', function( chunk ){
				data += chunk;
			});
			res.on('end', function(){
				cb(null, data);
			});
		}
		else
			cb(res.statusCode);
	});
	req.on('error', function(e){
		cb(e.message);
	});
	if(data)
		req.write(data);
	req.end();	
};
//////////////////////////////////////////////////////////////////
// get data
exports.get		= function( path, token, cb){
	var headers	= {};
	if( typeof(token) === 'function' ){
		cb	= token;
	}
	if( typeof(token) === 'object' ){
		for(var p in token)
			headers[p] = token[p];
	}
	exports.request( 'GET', path, headers, null, cb );
};
//////////////////////////////////////////////////////////////////
//	post data
exports.post	= function( path, data, token, cb ){
	var headers	= {};
	if( typeof(token) === 'function' ){
		cb	= token;
	}
	if( typeof(token) === 'object' ){
		for(var p in token)
			headers[p] = token[p];
	}
	headers['Content-Length']	= data.length;
	exports.request( 'POST', path, headers, data, cb );
};
//////////////////////////////////////////////////////////////////
// send file
exports.send_file	= function( path, file, token, cb ){
	var headers	= {};
	if( typeof(token) === 'function' ){
		cb	= token;
	}
	if( typeof(token) === 'object' ){
		for(var p in token)
			headers[p] = token[p];
	}
	headers['Content-Disposition']	= 'attachment;filename='+file.name;
	fs.readFile( file.path, function(err, data){
		if( err ) return cb(err);
		fs.unlink( file.path, function(err){
			if(err) return cb(err);
			exports.post( path, data, headers, cb );
		});
	});	
};
exports.check_status	= function( commands, token, cb ){
	var headers	= {};
	if(typeof commands === 'string' || typeof commands === 'number')
		commands	= [ commands ];
	if( typeof(token) === 'function' ){
		cb	= token;
	}
	if( typeof(token) === 'object' ){
		for(var p in token)
			headers[p] = token[p];
	}
	exports.get( '/commands/status?commands='+commands.join('+'), headers, cb);
};