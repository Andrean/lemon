
/*
*
*/

var mongoose	= require('mongoose');
var models	= {};
var entities	= {};
var service	= {};

// defining schemas
var serviceSchema	= {
		'id': String,
		'name': String,
		'type': String,
		'counter': Number,
		'state': String
	};
var entitySchema	= {
		'name': String ,	
		'entity_id':	{type: String, unique: true},
		'status':	String,
		'services':[serviceSchema]
	};

exports.init		= function(){
	entities	= mongoose.model( 'entities', entitySchema, 'entities' );
	services	= mongoose.model( 'services', serviceSchema, 'entity_services');
};
exports.getModels	= function(){
	models.entities	= entities;
	models.services	= services;
	return models;
};
