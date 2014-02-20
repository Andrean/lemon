/**
 * 		/models/data/trigger.js
 * 
 * 		Model of Trigger
 */

var mongoose	= require('mongoose');

var TriggerSchema	= mongoose.Schema({
	name:	{ type: String, trim: true },
	
});

TriggerSchema.set('collection','triggers');

module.exports	= mongoose.model('Trigger',TriggerSchema);