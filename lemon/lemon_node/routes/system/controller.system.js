/**
 *  Controller of all system operations
 */

exports.lemon	= {};
exports.lemon.get_status	= function( req, res ){
	req.query.commands;
	req.app.locals.lemon.check_status( req.query.commands, function( err, data){
		if(err){ console.log(err); res.send(500); return; }
		res.send( data );
	});
};