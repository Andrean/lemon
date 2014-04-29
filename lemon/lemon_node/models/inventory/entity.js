/**
 *  	/models/inventory/entity.js
 *  	Model of Entity
 */
var mongoose	= require('mongoose');

var EntitySchema	= mongoose.Schema({
	entity_id:	{ type: String, unique: true },
	agent:	 	{ type: mongoose.Schema.Types.ObjectId, ref: 'system.Agent' },
	info:		{
		name: 		{ type: String, "default": '', trim: true },
		description:{ type: String, "default": '', trim: true },
		_addedAt: 	{ type: Date,   "default": Date.now() }
	},
	data_items: [ {type: mongoose.Schema.Types.ObjectId, ref: 'data.DataItem'} ]
	// TODO: Здесь должен быть триггер, определяющий общее состояние Сущности по значениям всех data_items
});

EntitySchema.statics	= {
	load:	function( entity_id, cb ){
		this.findOne({ entity_id: entity_id })
			.populate( 'agent data_items' )
			.exec(cb);
	},
	list:	function( cb ){
		this.find({})
			.populate( 'agent data_items' )
			.exec(cb);
	}
};
EntitySchema.set('collection','entities');

module.exports	= mongoose.model('inventory.Entity',EntitySchema);