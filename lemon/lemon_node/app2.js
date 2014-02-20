/*
 * 	Main Expressjs application 
 * 
 */

var express = require('express')
			, config	= require('./config')
			, http = require('http')
			, path = require('path')
			, mongoose	= require('mongoose')
			, async		= require('async')
			, winston	= require('winston')
			, lemon		= require('./module.lemon');

/*winston.loggers.add('production',{
	console: {
		level: 'debug',
		colorize: true
	},
	file:	{
		filename: path.join(__dirname,'lemon.web.log'),
		json: false,
		level: 'debug'
	}
});
var logger	= winston.loggers.get('production');
var winstonStream = {
	    write: function(message, encoding){
	        logger.info(message);
	    }
	};
*/
function logErrors(err, req, res, next) {
	console.error(err.stack);
	next(err);
}
function clientErrorHandler(err, req, res, next) {
	if (req.xhr) {
		res.send(500, { error: 'Something blew up!' });
	} else {
		next(err);
	}
}
function errorHandler(err, req, res, next) {
    res.status(500);
	res.render('system_pages/500');
}
var app		= express();
var db		= mongoose.connection;

db.on("error", console.error.bind(console, "connection error:"));
db.once("open", function callback () {
    console.log("connected to mongodb at "+config.db);
});
mongoose.connect(config.db);

lemon.connect( config.lemon );
app.locals({
	  config: config,
	  lemon:  lemon
});
///////////////////////////////////////////////////////////////////////
// config
app.set('port', process.env.PORT || 80);
app.set('views', __dirname + '/views');
app.set('view engine', 'jade');
app.use(express.favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(express.logger('dev'));
app.use(express.bodyParser());
app.use(express.methodOverride());
app.use(express.static(path.join(__dirname, 'public')));
app.use(app.router);
app.use(logErrors);
app.use(clientErrorHandler);
app.use(errorHandler);
/////////////////////////////////////////////////////////////////////////

//load models
require('./models')( function(){
	// load routes and controllers
	require('./routes')( app );	
});

/////////////////////////////////////////////////////////////////////////
http.createServer(app).listen(app.get('port'), function(){
	  console.log('Express server listening on port ' + app.get('port'));
});
