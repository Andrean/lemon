/**
 *  Data model
 *  Agent 
 */

var mongoose	= require('mongoose');
var Schema		= mongoose.Schema;

var AgentSchema	= Schema({
	agent_id:	{ type: String, unique: true},
	name:		{ type: String, trim: true  },
	tags:	[ String ]
});
AgentSchema.statics	= {
	load: function(agent_id, cb){
		this.findOne( {agent_id: agent_id}, cb );
	},
	listByTag: function(tag, cb){
		this.find( {tags: tag})
			.sort('name')
			.exec(cb);
	},
	listExcludeTag: function( tag, cb){
		this.find( { tags: {$ne: tag} }, cb);
	}
};
AgentSchema.set('collection','agents');

module.exports	= function( __prefix__ ){	mongoose.model(__prefix__ + 'Agent',AgentSchema); };