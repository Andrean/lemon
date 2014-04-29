/**
 * 		/models/data/dataItems.js
 * 		Model DataItem
 */
var mongoose	= require('mongoose');

var DataItemSchema	= mongoose.Schema({
	name: 	{ type: String, trim: true, "default":'', required: true},
	entity: { type: mongoose.Schema.Types.ObjectId, ref: 'inventory.Entity' 	},
	type:   { type: String, lowercase: true, trim: true 			},
	contractor:	{ type: mongoose.Schema.Types.ObjectId, ref: 'data.Contractor'	},
	trigger:{ type: mongoose.Schema.Types.ObjectId, ref: 'data.Trigger'	},
	data:	{ type: mongoose.Schema.Types.ObjectId, ref: 'data.Data' 	},	
},	{
	autoIndex: false
});

var DataSchema	= mongoose.Schema({
	meta: [
	       {
	    	   chunk: 	{ type: mongoose.Schema.Types.ObjectId, ref: 'data.DataChunk' },
	    	   size: 	{ type: Number, min: 0, 'default':0	}, // size of chunk in Mb
	    	   count: 	{ type: Number, min: 0, 'default':0	},
	    	   range:   {
	    		   first: Date,
	    		   last:  Date
	    	   }
	       }
	   ]	
});

var DataChunkSchema	= mongoose.Schema({
	raw: [
	      {
	    	  timestamp: Date,
	    	  value: { type: mongoose.Schema.Types.Mixed, 'default': null }
	      }
	     ]
});

DataSchema.methods = { 
	findByTimeInterval: function( interval, cb ){ // interval = { start: _start_timestamp, end: _end_timestamp }
		this.find( 
				{ 
					data_id: this.data_id, 
					chunkNum: { $lt: this.chunkNum }, 
					'chunk.timestamp': { $gt: interval.start }, 
					'chunk.timestamp': { $lt: interval.end } 
				} 
			)
			.sort('chunkNum')
			.exec(function(err, data){
				if(err) return cb(err);
				var singleChunk	= [];
				for(var i in data)
					singleChunk = singleChunk.concat(data[i].chunk);
				data[0].chunk	= singleChunk.filter( function(item){
					if( interval.start < item.timestamp <= interval.end )
						return item;
				});
				cb(data[0]);
			});
	}
};

DataItemSchema.statics = {
	show: function( _id, cb ){
		this.findOne({id: _id})
			.populate('entity data trigger contractor')
			.exec(cb);
	}	
};

DataItemSchema.set('collection','data_item');
DataSchema.set('collection','data');
DataChunkSchema.set('collection','dataChunk');

module.exports	= function(__prefix__){
	__prefix__ = __prefix__ + '.';
	mongoose.model(__prefix__ + 'Data',DataSchema);
	mongoose.model(__prefix__ + 'DataItem',DataItemSchema);
	mongoose.model(__prefix__ + 'DataChunk',DataChunkSchema);
	
};