/**
 * Controller for agent routes
 */

var mongoose	= require('mongoose')
	, async		= require ('async')
	, Agent		= mongoose.model('system.Agent');

exports.list	= function( req, res, next){
	var tags	= (req.param('tag') || '').split(',');
	var exclude	= req.param('exclude') || '';
	var agents	= {excluded: [], data: []};	
	if(req.xhr){
		async.parallel([
		    function(callback){
			    async.map(
			    	tags,            
				    function(tag, cb){
				    	Agent.listByTag(tag, function( err, data){
				    		if(err) return cb(err);		    		
				    		cb(null, data || []);
				    	});
				    },
				    function(err, agents_by_tag){
				    	for(var i in agents_by_tag)
				    	{
				    		agents.data.push.apply(agents.data,agents_by_tag[i]);
				    	}	
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
		return;
	}
	///////////////////////////////////////////////////////////////////////////
	// not XMLHTTPRequest
	Agent.find({}, function(err, agents){
		if(err){ console.log(err); res.send(500); return; }
		res.render( 'agents/list', {title: "Agents", agents: agents, bg_color: "bg-color-Dark"} );
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
//////////////////////////////////////////////////////////////////////////
// /agents/:id/* handlers
//////////////////////////////////////////////////////////////////////////
exports.load_agent	= function( req, res, next ){
	Agent.findByAgentId( req.params.id, function(err, agent){
		if(err) return next(err);
		if(!agent) return exports.show_agentNotFound( req, res );
		res.agent	= agent;
		next();		
	});
};
exports.show_agentNotFound= function( req, res){
	res.render( 'agents/agent', { tiitle: "Agent not found", bg_color: 'bg-color-Dark', action: 'not'});
};
exports.show_one	= function( req, res ){
	res.render( 'agents/agent', { title: "Agent - " + res.agent.name, agent: res.agent, bg_color: 'bg-color-Dark' });	
};

exports.show_update	= function( req, res ){
	res.render( 'agents/agent.update.jade', { title: "Agent update - " + res.agent.name, agent: res.agent, bg_color: 'bg-color-Dark' });
};