/**
 * 		/models/data/contractor.js
 * 
 * 		Model of Contractor
 */
var mongoose	= require('mongoose');

var ContractorSchema	= mongoose.Schema({
	name:		{ type: String, trim: true 		},
	content: 	{ type: String, 'default': ''	},
	version: 	{ type: Number, min: 0, 'default':0	}
});
ContractorSchema.set('collection','contractors');

module.exports	= function(__prefix__){	mongoose.model(__prefix__ + '.'+'Contractor', ContractorSchema); };
