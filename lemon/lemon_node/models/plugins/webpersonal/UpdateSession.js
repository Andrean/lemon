



var mongoose	= require('mongoose');
var Schema		= mongoose.Schema;

var UpdateSessionSchema	= new Schema({
	info_system: 	{ type: String, trim: true, match: /.+/ },
	services:		[
	         { type: String, trim: true}
	        ],
	distr:	{
		filename:	String,
		name:		String
	},
	history: {
		begin:	{	type: Number     },
		end:				Number,
		load_distr: 		Number,
		switch_fronts: 		Number,
		switch_services: 	Number,
		distribute_files: 	Number
	},
	stamp:	String,
	session_id: String	
});

UpdateSessionSchema.statics	= {		
		load:	function(cb)	{
			this.find( {}, cb );		
		},
		findBySystem: function( info_system, cb ){
			this.find({ info_system: info_system}, cb );
		},
		findBySession: function( session_id, cb){
			this.findOne( {session_id: session_id} ,cb );
		}
	};
UpdateSessionSchema.set('collection', 'update.sessions');

function load( __prefix__ ){
	mongoose.model(__prefix__ + 'UpdateSession',UpdateSessionSchema);
} 

module.exports	= load;
