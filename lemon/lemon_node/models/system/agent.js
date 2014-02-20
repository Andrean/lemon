/**
 *  Data model
 *  Agent 
 */

var mongoose	= require('mongoose');
var Schema		= mongoose.Schema;

var AgentSchema	= Schema({
	agent_id:	{ type: String, unique: true},
	name:		{ type: String, trim: true  },
	tags:	[ String ],
	entities:	[ {type: mongoose.Schema.Types.ObjectId, ref: 'inventory.Entity'} ]
});
AgentSchema.statics	= {
	load: function(agent_id, cb){
		this.findOne( {agent_id: agent_id})
			.populate('entities')
			.exec(cb);
	},
	listByTag: function(tag, cb){
		this.find( {tags: tag})
			.populate('entities')
			.sort('name')
			.exec(cb);
	},
	listExcludeTag: function( tag, cb){
		this.find( { tags: {$ne: tag} })
			.populate('entities')
			.exec(cb);
	},
	findByAgentId: function( agent_id, cb){
		this.findOne({agent_id: agent_id})
			.populate('entities')
			.exec(cb);
	}
};
AgentSchema.set('collection','agents');

module.exports	= function( __prefix__ ){	mongoose.model(__prefix__ + 'Agent',AgentSchema); };