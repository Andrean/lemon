/**
 * 		Model Plugina
 * 
 * 		Plugin is additional functionality entity
 */

var mongoose = require('mongoose');

var PluginSchema	= mongoose.Schema({
		name:		{ type: String, unique: true, trim: true},
		version: 	{ type: Number},
		enabled: 	{ type: Boolean},
		files: 		[ { type: String } ],
		main:		{ type: String }
});
PluginSchema.set('collection','plugins');

module.exports	=	function(__prefix__){	mongoose.model(__prefix__ + 'Plugin',PluginSchema); };
	