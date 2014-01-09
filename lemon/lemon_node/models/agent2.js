

var mongoose	= require('mongoose');
var models	= {};
var agents	= {};


exports.init		= function(){
	agents	= mongoose.model('standard_agents',
			{	
				'dns_name': String, 
				'short_name': String,
				'agent_id': {type: String, unique: true}, 
				'status': String, 
				'service_name': String, 
				'service_type': String
			});
};
exports.getModels	= function(){
	models.standard_agents	= agents;
	return models;

};



