
var agents	= {};

exports.init	= function(){
	agents		= global.models.agents.standard_agents;
};

exports.index = function(req, res){
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