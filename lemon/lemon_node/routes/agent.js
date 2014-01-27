/**
 * Controller for agent routes
 */

var mongoose	= require('mongoose')
	, async		= require ('async')
	, Agent		= mongoose.model('Agent');

exports.list	= function( req, res, next){
	var tags	= (req.param('tag') || '').split(',');
	console.log(tags);
	var exclude	= req.param('exclude') || '';
	var agents	= {excluded: [], data: []};	
	async.parallel([
	    function(callback){
		    async.map(
		    	tags,            
			    function(tag, cb){
			    	Agent.listByTag(tag, function( err, data){
			    		if(err) return cb(err);		    		
			    		cb(null, data[0] || []);
			    	});
			    },
			    function(err, agents_by_tag){
			    	agents.data	= agents_by_tag;
			    	callback();
			    }
			);			
	    },
	    function(cb){
	    	Agent.listExcludeTag(exclude, function(err, data){
	    		if(err) return cb(err);
	    		agents.excluded	= data || [];
	    		cb();
	    	});
	    }
	], function(err){
		res.send(agents);
	});
	
};
exports.modify	= function( req, res ){
	async.each(
		req.body.agents, 
		function(item, cb){
			console.log(item);
			Agent.update({ agent_id: item.agent_id },{ $addToSet:{ tags: { $each: item.tags }}}, function(err){
				if(err) return cb(err);
				cb();
			});
		},
		function(err){
			if(err) throw err;
			res.send(200);
		}
	);
};