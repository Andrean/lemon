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
			, winston	= require('winston');

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
var app		= express();
var db		= mongoose.connection;

db.on("error", console.error.bind(console, "connection error:"));
db.once("open", function callback () {
    console.log("connected to mongodb at "+config.db);
});
mongoose.connect(config.db);

app.locals({
	  config: config
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
app.use(express.errorHandler());
/////////////////////////////////////////////////////////////////////////

//load models
var a = require('./models');
// load controllers
var b = require('./controllers')( app, function(){
	// load routes
	require('./routes')( app );
} );

/////////////////////////////////////////////////////////////////////////
http.createServer(app).listen(app.get('port'), function(){
	  console.log('Express server listening on port ' + app.get('port'));
});
