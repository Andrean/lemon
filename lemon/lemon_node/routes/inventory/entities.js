
var 	entities	= {}
	  ,	e_services	= {}
	  , uuid	= require('uuid');
	
var entity_requestHandler	= function( req, callback ){
	if(req.params.id)
	{
		entities.findOne({'entity_id': req.params.id}, function(err, result){
				console.log("result: "+result);
				if(err)
					callback(err);
				else
					callback(err, result);				
			} 
		);	
	}
	else
	{
		entities.find({}, function(err, results){
				console.log("result: "+results);
				if(err)
					callback(err);
				else
					callback(err, results);				
			} 
		);	
	}
};

var init	= function(){
	e_services	= global.models.entity.services;
	entities	= global.models.entity.entities;
};

var entity_fn	= function(req, res){
	console.log("Performed entity info request");
	entity_requestHandler( req, function( err, result ){
		if(err)
			console.log(err);
		else{
			entity_result = result;
			if(req.xhr)
				res.send(entity_result);
			else{
				console.log(entity_result);
				res.render('entity_info', {bg_color: 'bg-color-purple', entity: result});
			}
		}
	});

};
var entity_add	= function(req, res){
	var name	= req.param(name);
	if(req.query.name)
		name = req.query.name;
	var _e	= new entities( {	
								'entity_id': uuid.v1(), 
								'name': name,
								'status': 'OK',
								'services':[]
							}
	);
	_e.save( function(err, _e){
		if(err)
		{
			console.log("Error while add new entity: " + err);
			res.send(500, 'not saved');
		}
		else
		{
			if(req.xhr)
				res.send(_e);
			else
				res.render('entity_info', {bg_color: "bg-color-purple", entity: _e});
		}
	});

};
var entity_group	= function(req, res){
	
};

var show_allEntities	= function( req, res ){
	entities.find({} ,function(err, results){
		var tiles	= [];
		for( var item in results )
		{
			var tile	= {	'id': 'entity_tile'+(results[item].entity_id),	
							'class': 'tile outline-color-yellow', 
							'subclass': 'tile-content',
							'entity_name': results[item].name,
							'entity_status': results[item].status,
			};
			tiles.push(tile);
			console.log(tile);
		}
		res.render('entities_list', {
			bg_color: "bg-color-purple",
			tiles: tiles
		});
	});
};



exports.init	= init;
exports.group	= entity_group;
exports.entity	= entity_fn;
exports.add_entity	= entity_add;
exports.show_all	= show_allEntities;