
/**
 * Module dependencies.
 */

var express = require('express')
  , routes = require('./routes')
  , user = require('./routes/user')
  , test = require('./routes/test')
  , systemPages = require('./routes/system')
  , entities	= require('./routes/inventory/entities')
  , groups		= require('./routes/inventory/groups')
  , administration = require('./routes/administration')
  , http = require('http')
  , path = require('path') 
  , mongoose = require('mongoose');
  
var models		= {};
var app 		= express();


models.agents	= require('./models/agent');
models.entity	= require('./models/entity');
models.agent_manager	= require('./models/agent_manager');
models.files	= require('./models/files.js')
/*
var model_agent		= require('./models/agent');
var model_entity	= require('./models/entity');
var model_agent_manager	= require('./models/agent_manager')
*/  
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
app.use(express.favicon(path.join(__dirname, 'public/favicon.ico')));
app.use(express.logger('dev'));
app.use(express.bodyParser());
app.use(express.methodOverride());
app.use(express.static(path.join(__dirname, 'public')));
app.use(app.router);

// development only
if ('development' == app.get('env')) {
  app.use(express.errorHandler());
}

global.models	= {};

app.get('/', routes.index);
app.get('/users', user.list);
app.get('/test', test.test);
app.get('/test/:method', test.test);
//app.get('/inventory/entities/groups/:group', entities.group);
//app.get('/inventory/entities/add', entities.add_entity);
app.get('/inventory/entities/:id/tasks', entities.manage_tasks);
app.post('/inventory/entities/:id/tasks', entities.tasks);
app.get('/inventory/entities/:id', entities.entity);
app.get('/inventory/entities', entities.show_all);
//app.post('/inventory/entities', entities.add_entity);
app.post('/inventory/entities/contractor', entities.upload_contractor);
app.get('/inventory/entities/:id/contractors',entities.contractors_get);
app.get('/inventory/entities/:id/agent',entities.agent_get);
app.post('/inventory/entities/:id/agent',entities.agent_post);
app.post('/inventory/entities/contractors',entities.contractors_post);
app.get('/inventory/entities/:id/test',entities.test);
app.post('/inventory/entities/task', entities.setup_scheduler_task);
app.post('/inventory/entities/:id', entities.get_contractors);
app.get('/inventory/entities/:id/data', entities.get_data);
app.get('/inventory/entities/:id/tags', entities.get_tags);
app.get('/inventory/groups', groups.get)
app.get('/administration/update', administration.update)
app.get('/administration/update/:service', administration.update)
app.get('*',systemPages.get404);


// initializing models
for(var m in models){
	models[m].init();
	console.log(models[m]);
	global.models[m] = models[m].getModels();
	console.log(m);
}

routes.init();
entities.init();
test.init();

http.createServer(app).listen(app.get('port'), function(){
  console.log('Express server listening on port ' + app.get('port'));
});
