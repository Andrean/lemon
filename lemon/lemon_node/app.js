
/**
 * Module dependencies.
 */

var express = require('express')
  , routes = require('./routes')
  , user = require('./routes/user')
  , test = require('./routes/test')
  , entities	= require('./routes/inventory/entities')
  , http = require('http')
  , path = require('path') 
  , mongoose = require('mongoose');
  
var models		= {};
var app 		= express();

var model_agent		= require('./models/agent');
var model_entity	= require('./models/entity');
  
mongoose.connect('mongodb://test-note.kontur/mydb');
var db	= mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));

global.mongoose		= mongoose;
global.db			= db;
global.app			= app;

// all environments
app.set('port', process.env.PORT || 8080);
app.set('views', __dirname + '/views');
app.set('view engine', 'jade');
app.use(express.favicon());
app.use(express.logger('dev'));
app.use(express.bodyParser());
app.use(express.methodOverride());
app.use(app.router);
app.use(express.static(path.join(__dirname, 'public')));

// development only
if ('development' == app.get('env')) {
  app.use(express.errorHandler());
}

global.models	= models;

app.get('/', routes.index);
app.get('/users', user.list);
app.get('/test', test.test);
app.get('/test/:method', test.test);
app.get('/inventory/entities/groups/:group', entities.group);
app.get('/inventory/entities/add', entities.add_entity);
app.get('/inventory/entities/:id', entities.entity);
app.get('/inventory/entities', entities.show_all);
app.post('/inventory/entities', entities.add_entity);

// initializing models
model_agent.init();
model_entity.init();
global.models.agents	= model_agent.getModels();
global.models.entity	= model_entity.getModels();

routes.init();
entities.init();
test.init();

http.createServer(app).listen(app.get('port'), function(){
  console.log('Express server listening on port ' + app.get('port'));
});
