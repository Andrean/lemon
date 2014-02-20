/**
 * 		/models/data/dataItems.js
 * 		Model DataItem
 */
var mongoose	= require('mongoose');

var DataItemSchema	= mongoose.Schema({
	name: 	{ type: String, trim: true, "default":'', required: true},
	entity: { type: mongoose.Schema.Types.ObjectId, ref: 'Entity' 	},
	data:	{ type: mongoose.Schema.Types.ObjectId, ref: 'Data' 	}, // hold document of Data with chunkNum: 0.
	type:   { type: String, lowercase: true, trim: true 			},
	contractor:	{ type: mongoose.Schema.Types.ObjectId, ref: 'Contractor'	},
	trigger:{ type: mongoose.Schema.Types.ObjectId, ref: 'Trigger'	}
},	{
	autoIndex: false
});

var DataSchema	= mongoose.Schema({
	data_id: 	{ type: String, lowercase: true, trim: true },
	chunkNum: 	{ type: Number, min: 0 },
	chunk:		[{ type: mongoose.Schema.Types.Mixed }]	
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

module.exports	= function(__prefix__){
	__prefix__ = __prefix__ + '.';
	mongoose.model(__prefix__ + 'Data',DataSchema);
	mongoose.model(__prefix__ + 'DataItem',DataItemSchema);
};