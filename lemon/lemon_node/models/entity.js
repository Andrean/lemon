
/*
*
*/

var mongoose	= require('mongoose');
var models	= {};
var entities	= [];
var service	= {};
var entityList	= {};

// defining schemas
var contractorSchema	= {
		'__id': String,
		'name': String,
		'result': String,
		'args': [String],
		'path': String,
		'state': Number,
		'exit_code': Number,
		'duration_time': Number,
		'start_time':Number
	};
var serviceSchema	= {
		'__id': String,
		'name': String
	};
var schedulerTaskSchema	= {
	'__id': String,
	'name': String,
	'last_time': Number,
	'start_time': Number,
	'interval': Number,
	'task': {}
};
var agentSchema		= {
		'agent_id':	 String,
		'state': String,
		'start_time': Number,
		'end_time': Number,
		'scheduler': [schedulerTaskSchema]
	};
var entitySchema	= {
		'entity_id': String,
		'time': 	Number,
		'agent':	agentSchema,
		'data':		[contractorSchema],		
		'name':		String,
		'install':  {type: Boolean, default: false}
	};
var dataSchema	={
		'entity_id': String,
		'time':	Number,
		'data': [contractorSchema]
};

exports.init		= function(){
	entities	= mongoose.model( 'entities', entitySchema, 'entities' );
	data		= mongoose.model( 'data', dataSchema, 'data');	
};
exports.getModels	= function(){
	models.entities	= entities;
	models.data	= data;
	return models;
};
