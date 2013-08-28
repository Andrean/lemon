/*
*	Contractors and scheduler task for run contractors
*
*/




var mongoose	= require('mongoose');
var models		= {};

var ContractorCollection	= 'contractors'
var SchedulerTaskCollection	= 'agent_scheduler'
var groupsCollection		= 'groups'
var configurationCollection	= 'configuration'

var groupsSchema		= {
		'agent_id': String,
		'tag': String
	}
var configurationSchema	= {
		'__id': {type: String, unique: true},
		'__type': String,
		'__added': Number,
		'__tags': [String],
		'__revision': {type: Number, default: 0},
		'__enabled': {type: Boolean, default: false},
		'content':  {}
	}
var contractorSchema	= {
		'id': String,
		'name': {type: String, unique: true},
		'content': String,
		'deleted': {type: Boolean, default: false},
		'modified': {type: Boolean, default: true},
		'install': {type: Boolean, default: false}
	};
var argsSchema	= {
		'contractor': String,
	}
var taskSchema	= {
		'id': String,
		'name': {type: String, unique: true},
		'interval': Number,
		'start_time': Number,
		'func': String,
		'modified': {type: Boolean, default: true},
		'deleted': {type: Boolean, default: false},
		'install': {type: Boolean, default: false},
		'kwargs': argsSchema
	};
	
exports.init	= function(){
	contractors	= mongoose.model(ContractorCollection, contractorSchema)
	tasks		= mongoose.model(SchedulerTaskCollection, taskSchema, SchedulerTaskCollection)
	groups		= mongoose.model(groupsCollection, groupsSchema, groupsCollection)
	configuration = mongoose.model(configurationCollection, configurationSchema, configurationCollection)
}

exports.getModels	= function(){
	models.contractors	= contractors;
	models.tasks		= tasks;
	models.groups		= groups;
	models.configuration	= configuration;
	return models;
}