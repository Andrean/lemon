/**
 * Data model 
 * Service Map
 */

var mongoose	= require('mongoose');
var Schema		= mongoose.Schema;

var ServiceMapSchema	= new Schema({
	type:			{ type: String, trim: true, default: 'map' },
	info_system: 	{ type: String, trim: true, unique: true, match: /.+/ },
	name:			{ type: String, trim: true },
	sm_port:		{ type: Number},
	iis_site:		{ type: String, trim: true},
	map: [{
		services: [ 
		    { 
		    	name: { type: String, trim: true},
		    	settings: [
		    	    {
		    	    	name: { type: String, trim: true},
		    	    	fileName: { type: String, trim: true}
		    	    }
		    	]
		    } 
		],
		path:		{ type: String, trim: true },
		tag: 		String
	}],
	services: [ 
	    {
	    	name: { type: String, trim: true },
	    	settings: [ { type: String, trim: true } ]
	    } 
	],	
	
});

ServiceMapSchema.statics	= {		
	load:	function(name, cb)	{
		this.findOne( {type: 'map', info_system: name}, cb );		
	},
	load_all: function(cb){
		this.find( {type: 'map'}, cb);
	}
};
ServiceMapSchema.set('collection', 'service_map');

function load( __prefix__ ){
	mongoose.model(__prefix__ + 'ServiceMap',ServiceMapSchema);
} 
module.exports	= load;
