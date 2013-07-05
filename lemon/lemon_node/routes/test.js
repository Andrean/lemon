
var jade	= require('jade');
var testers	= {};
var agents	= {};

exports.init	= function(){
	testers 	= global.models.testers;
	agents		= global.models.agents.standard_agents;
};

exports.test = function(req, res){
	if(req.params.method == 'add')
	{
		var agent1 = new agents({	'short_name': req.query.short_name, 
								'agent_id': req.query.id, 
								'status':req.query.status,
								'dns_name': req.query.dns_name,
								'service_name':'agent_service_1', 
								'service_type':'test_type'});
		agent1.save(function(err, agent1){
			if(err)
				console.log(err.code + '\n' + err.err);
		});
	}
	var query	= agents.find({} ,function(err, results){
		var tiles	= [];
		var id = 1;
		for( var item in results )
		{
			var tile	= {	'id': id++,	
							'class': 'tile outline-color-yellow', 
							'subclass': 'tile-content',
							'agent-short-name': results[item].short_name,
							'agent-status': results[item].status,
							'agent-dns-name' : results[item].dns_name
							};
			tiles.push(tile);
		}
		if(req.xhr)
		{
			console.log('Performed XMLHttpRequest');
			res.send(tiles);/*
			res.render('server_tile', {
					agents: results, tile_id: tile_id
				});*/
		}
		else
		{
			res.render('test', {bg_color: "bg-color-purple"});
		}
	});

};