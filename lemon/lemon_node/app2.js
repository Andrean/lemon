/*
 * 	Main Expressjs application 
 * 
 */

var express = require('express')
			, config	= require('./config')
			, http = require('http')
			, path = require('path')
			, mongoose	= require('mongoose');

var app		= express();
var db		= mongoose.connection;

db.on("error", console.error.bind(console, "connection error:"));
db.once("open", function callback () {
    console.log("connected to mongodb at "+config.db);
});
mongoose.connect(config.db);


// load models
require('./models/ServiceMap');
require('./models/Agent');

// load routes

var wp   = require('./routes/webpersonal')
	, agent	= require('./routes/agent');

app.locals({
	  config: config
});
// config
app.set('port', process.env.PORT || 80);
app.set('views', __dirname + '/views');
app.set('view engine', 'jade');
app.use(express.favicon(path.join(__dirname, 'public/favicon.ico')));
app.use(express.logger('dev'));
app.use(express.bodyParser());
app.use(express.methodOverride());
app.use(express.static(path.join(__dirname, 'public')));
app.use(app.router);
app.use(express.errorHandler());

/* 
 * 	routes 
 */
app.get('/', function( req, res ){	res.redirect('/webpersonal'); });
// webpersonal functions
app.param('service'	, wp.loadServiceMap);	// returns req.map
app.all( '/webpersonal(/*)?', 	wp.loadSystems					);
app.get( '/webpersonal',		wp.main_view					);	
app.get( '/webpersonal/update/:service?'		, wp.view 		);
app.post('/webpersonal/update/:service/upload'	, wp.upload 	);
app.post('/webpersonal/update/:service/setup'	, wp.setup		);
app.get( '/webpersonal/update/:service/status'	, wp.get_status	);
app.post( '/webpersonal/update/:service/switch_services', wp.switch_services	);
app.post( '/webpersonal/update/:service/switch_fronts'	, wp.switch_fronts		);
app.get( '/webpersonal/configure/:service?'		, wp.configure	);
app.post('/webpersonal/configure/:service/map'	, wp.edit_map	);
app.del('/webpersonal/configure/:service/map'	, wp.del_map	);
app.post('/webpersonal/configure/:service/system', wp.edit_system_map);
app.get( '/webpersonal/configure/:service/services'	, wp.services		);
app.post('/webpersonal/configure/:service/services'	, wp.edit_services	);
app.put( '/webpersonal/projects/new',	wp.projects_new			);
app.get( '/webpersonal/settings/pull',	wp.git_pull);
// common routes
app.get( '/agents',		agent.list			);
app.post('/agents',		agent.modify		);


/////////////////////////////////////////////////////////////////////////
http.createServer(app).listen(app.get('port'), function(){
	  console.log('Express server listening on port ' + app.get('port'));
});
