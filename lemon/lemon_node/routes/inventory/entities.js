
var 	entities	= {}
	  ,	e_services	= {}
	  , uuid	= require('uuid'),
	  fs	= require('fs');
	  
	
var entity_requestHandler	= function( req, callback ){
	if(req.params.id)
	{
		entities.findOne({'entity_id': req.params.id}, function(err, result){
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
				if(err)
					callback(err);
				else
					callback(err, results);				
			} 
		);	
	}
};

var computeSize	= function(size_bytes){
		result	= size_bytes + " bytes"
		return result
	}
var init	= function(){
	data		= global.models.entity.data;
	entities	= global.models.entity.entities;	
	contractors	= global.models.agent_manager.contractors;
	tasks		= global.models.agent_manager.tasks;
	groups		= global.models.agent_manager.groups;
	configuration		= global.models.agent_manager.configuration;
	collFiles		= global.models.files.files;
	collCommands	= global.models.agent_manager.commands;
};
var error	= function(err_msg){
	console.log('ERROR: '+err_msg) 
	
}
function _error(err_msg, response){
	console.log('ERROR: '+err_msg) 
	response.send(500, {error: err_msg})
}
var entity_fn	= function(req, res){
	if(req.xhr){
		answer	= {'status': 'error', 'time': 0}
		id	= req.params.id
		install	= req.query.install
		sdelete	= req.query.delete
		stime	= req.query.time
		if(id)
		{
			if(stime){
				entities.findOne({'entity_id': id}, function(err, result){
					if(err)
						console.log(err)
					else{
						answer.status	= 'ok'
						answer.time	= result.time
						res.send(answer)						
					}
				})
			}
			if(install && sdelete){
				res.send(answer)
				return
			}
			if(install)
				entities.findOne({'entity_id': id}, function(err, result){
					if(err)
						console.log(err)
					else{
						if(install == 1)
							result.install	= true;
						if(install == 2)
							result.install	= false;
						result.save()
						answer.status	= 'ok'
						res.send(answer)
					}
				})
			if(sdelete)
			{
				entities.findOne({'entity_id': id}, function(err, result){
					if(err)
						console.log(err)
					else{
						if(result){
							result.remove()
							answer.status = 'removed'}
						res.send(answer)
					}
					
				})
			}
		}
		else
			res.send(answer)
	}
	else {
		console.log("Performed entity info request");
		entity_requestHandler( req, function( err, result ){
			if(err)
				console.log(err);
			else{
				entity_result = result;
				records	= [];
				res.render('entity_info', {bg_color: 'bg-color-blueDark', entity: result, records: records});
			}
		});
	}
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
			var host_info	= {}
			var data	= results[item].data
			for(var c in data)
				if(data[c].name == 'getHostInfo')
					host_info	= JSON.parse(data[c].result)									
			var name	= results[item].entity_id;
			var status	= 'NO DATA'
			if(host_info){
				if(host_info.computersystem)
					if(host_info.computersystem[0].Caption)
					{
						name	= host_info.computersystem[0].Caption
						results[item].name	= name
						results[item].save()
					}
				if(host_info.computersystem)
					if(host_info.computersystem[0].Status)
						status	= host_info.computersystem[0].Status
			}
			var tile	= {	'id': 'entity_tile'+(results[item].entity_id),	
							'class': 'tile outline-color-yellow', 
							'subclass': 'tile-content',
							'entity_name': name,
							'entity_status': status,
							'installed': results[item].install
			};
			tiles.push(tile);			
		}
		res.render('entities_list', {
			bg_color: "bg-color-blueDark",
			tiles: tiles
		});
	});
};
function updateRevision(){
	configuration.findOne({'__type':'revision'}, function(err, result){
		if(err)
			console.log(err)
		else{
			if(result)
				result.__revision +=1
			else
				result = new configuration({
					'__id' : String(uuid.v1()),
					'__type': 'revision',
					'__added': (new Date()).getTime(),
					'__tags': [],
					'content' : { 'revision' : 1}
				})
			result.save()
		}
	})
}
function _createContractor(name, data, args){
	return {
		'id' : String(uuid.v1()),
		'name':name,
		'content': data,
		'args': args
	}
}
function _createScheduledTask(s){
	return {
		'id': String(uuid.v1()),
		'name':	s.name,
		'func': s.func,
		'interval': parseInt(s.interval || 0),
		'start_time': parseInt(s.start || 0),
		'description': s.description || "",
		'kwargs': {'contractor': s.contractor}
	}
}
function _addConfigurationItem(type, content, tag){
	updateRevision()
	if(!tag) tag = 'default'
	return new configuration({
					'__id' : String(uuid.v1()),
					'__type': type,
					'__added': (new Date()).getTime(),
					'__tags': [tag],
					'__enabled': false,
					'content': content
					})
}
function _upload(type, item, tag){
	
}

var contractors_get		= function(req, res){
	var id	= req.params.id
	groups.findOne({'agent_id': id}, function(err, tag_record){
		if(err) return error(err)
		var tag	= tag_record.tag
		var list	= []
		configuration.find({'__tags': tag, '__type': 'contractor'}, function(err, c_list){
			if(err) return error(err, res)
			entities.findOne({'entity_id': id}, function(err, _entity){
				if(err) return error(err, res)
				var data	= _entity.data
				var it = 0
				var _d	= {}
				for(var _it in data){
					it	= data[_it]
					_d[it.name] = it
				}
				for(var _it in c_list){
					var _c	= {'name': "", 'size': 0, 'added': 0, 'enabled': false, 'revision':0, 'tags':[]}
					it	 		= c_list[_it]
					_c.name		= it.content.name
					_c.size		= it.content.content.length
					_c.added	= it.__added
					_c.enabled	= it.__enabled
					_c.revision	= it.__revision
					_c.tags		= it.__tags
					_c.data		= _d[_c.name]
					list.push(_c)				
				}
				res.send({'response': list})
			})
			
		})
	})
	
	
}
var contractors_post	= function(req, res){
	var files	= req.files
	var del		= req.body.delete
	var name	= req.body.name
	var args	= req.body.args || []
	var change	= req.body.change
	var enable	= req.body.enable
	var update	= req.body.update
	var type	= 'contractor' 
	var status	= {'status': 'error'}
	updateRevision()
	if(change)
		configuration.findOneAndUpdate({'__type': 'contractor', 'content.name': name}, {'__enabled': enable}, function(err, result){
			if(err){error(err); res.send(status);return;}
			status.status='ok'
			res.send(status)
		})
	if(files)
	{
		var file	= files.file
		var name	= file.name.match(/\w+/)[0]
		fs.readFile(file.path, function(err, data){
			if(err){ error(err); res.send(status); return }
			configuration.find({'__type': 'contractor', 'content.name': name}, function(err, results){
				if(err){ error(err); res.send(status); return }
				if(results.length < 1){
					var c	= _addConfigurationItem(
												'contractor',
												_createContractor(name, String(data), args)
											)
					c.save(function(err, result){
						if(err){ error(err); res.send(status); return;}
						status.status	= 'ok'
						status.name	= result.content.name
						status.size	= computeSize(result.content.content.length)
						res.send(status)
					})
				}
				else
					if(!update)
						res.send(status)
					else{
						if(results.length == 1){
							var item = results[0]
							item.content.content	= String(data)
							item.__revision	= item.__revision + 1
							item.save(function(err, r){
								if(err) { error(err); res.send(status); return;}
								status.status = 'ok'
								status.name	= r.content.name
								status.revision	= r.__revision
								status.size	= computeSize(r.content.content.length)
								res.send(status)								
							})
						}
					}
			})			
		})
	}
	if(del){
		if(name)
		{
			configuration.remove({'__type': 'contractor', 'content.name': name}, function(err, result){
				if(err) return error(err);
				status.deleted = true
				status.status  = 'ok'
				res.send(status)
			})
		}
	}
}

var uploadContractor	= function(req, res){
	if(req.files)
	{
		var file	= req.files.file;
		fs.readFile(file.path, function(err, data){
			if(err)
				console.log(err);
			else
			{
				var cntr = _addConfigurationItem(	'contractor', 
													_createContractor(file.name.match(/\w+/)[0], String(data))
												)
				cntr.save(function(err, result){
					if(err){
						console.log(err)
						res.send("none")
						}
					else{
						configuration.count({}, function(e, count){
							record	= {'row_number': count-1, 'name': result.content.name, 'size': computeSize(result.content.content.length),'install': result.__enabled}
							res.render('entity_filerow', {'record': record})
						})
					}
				})
			}
		
		});		
	}
	else{
		install	= req.body.install;
		name	= req.body.name;
		if(install == 'true'){
			configuration.findOneAndUpdate({'__type':'contractor',"content.name":name},{'__enabled': true},function(err, result){
				status	= 'installed';
				if(err){
					status	='error'
					console.log(err)
					}
				res.send({'status':status})				
			})
		}
		else{
			configuration.remove({'__type': 'contractor',"content.name": name}, function(err, result){
				if(err) console.log(err)
				else{
					updateRevision()
					res.send({'status':'deleted'})
					}
			})
		}
	}
	
	
};
var getContractors	= function(req, res){
	arg	= req.body.contractor
	if(arg=='get')
	{
		configuration.find( {'__type':'contractor'}, function(err, results){
			if(err)
				console.log(err)
			else{
				records	= []
				for(var i in results){
					tmp	= { 'row_number': 0, 'name': "", 'size': ""}
					tmp.row_number	= i;
					tmp.name		= results[i].content.name;
					tmp.size		= results[i].content.content.length;
					tmp.size		= computeSize(tmp.size)
					tmp.install		= results[i].__enabled;
					r = configuration.findOne({'__type':'scheduled_task','content.kwargs.contractor': tmp.name}, function(err, data){
						if(data){
							tmp.task_name	= data.content.name
							tmp.task_interval	= data.content.interval							
						}								
						
						
					})
					records.push(tmp)
				}				
				res.render('entity_filerows', {records: records});
						
			}
		})
		

	}
	else{
		res.send({'null':true})
	}
};
var setupTask	= function(req, res){
	console.log(req.body)
	disable	= req.body.disable
	t_name	= req.body.task_name
	t_interval	= req.body.interval
	t_contractor	= req.body.contractor
	t_start_time	= req.body.start_time
	if(!t_interval){
		t_interval	= 0;
		t	= t_start_time.match(/(\d+)\-(\d+)\-(\d+)T(\d+):(\d+)/)
	}
	else{
		t	= t_interval.match(/(\d+)/)
		t_interval	= t[1]
	}
	if(disable){
		configuration.findOneAndUpdate({'__type':'scheduled_task','content.name': t_name},{'__enabled':false}, function(err,result){
			if(err)
			{
				console.log(err)
				res.send({'status': 'error'})
			}
			else
				res.send({'status':'disabled'})
		})
		
	}
	else{
	
		var task	= _addConfigurationItem(	'scheduled_task', 
												_createScheduledTask(t_name, t_interval, t_start_time, t_contractor)
											)
		task.__enabled	= true
		task.save(function(err,result){
			if(err){
				console.log(err)
				res.send({'status':'error'})
			}
			else{
				updateRevision()
				res.send({'status':'ok', 'name': result.content.name, 'interval': 0})
			}
				
		})
	}
}
var tasks		= function(req, res){
	if(req.xhr){
		var id	= req.params.id
		var install		= req.body.install
		var disable		= req.body.disable
		var enable		= req.body.enable
		var uninstall	= req.body.uninstall
		var settings	= {}
		settings.name			= req.body.name
		settings.interval		= req.body.interval
		settings.start			= req.body.start
		settings.contractor		= req.body.contractor
		settings.description	= req.body.description
		settings.func			= req.body.func
		var response	= {'status': 'error'}
		if(install){
			configuration.findOne({'__type':'scheduled_task','content.name':settings.name}, function(err, result){
				if(err) return error(err, res);
				if(result){
					response.status='alert'
					response.msg='task is exists'
					res.send(response)
					return
				}
				var task	= _addConfigurationItem(	'scheduled_task',
														_createScheduledTask(settings),
														id
								)
				task.__enabled	= true
				task.save(function(err, result){
					if(err) return error(err, res);
					response.status	= 'ok'
					res.send(response)
				})
			})
			return
		}
		if(disable || enable){
			configuration.findOneAndUpdate({'__type':'scheduled_task','content.name':settings.name},{'__enabled': enable || false}, function(err, result){
				if(err) return error(err, res);
				response.status='ok'
				res.send(response)
			})
			return
		}
		if(uninstall){
			configuration.remove({'__type':'scheduled_task','content.name':settings.name}, function(err, result){
				if(err) return error(err ,res)
				response.status	= 'ok'
				res.send(response)
			})
			return
		}
		
		return
	}
	res.send('not XmlHTTPRequest')
}
var manageTasks	= function(req, res){
	deleteID	= req.query.delete
	installID	= req.query.install
	show_agent		= req.query.show_agent
	id	= req.params.id
	if(deleteID){
		configuration.remove({'__type': 'scheduled_task', 'content.id':deleteID}, function(err, result){
			if(err){ console.log("Error: "+err)
				res.send({'status': 'error'})
			}
			else {
				res.send({'status': 'removing'})
			}
		})
		return
	}
	if(show_agent==1){
		entities.findOne({'entity_id': id}, function(err, result){
			if(err)		console.log(err)
			else	{
				scheduler	= result.agent.scheduler
				_tasks	= []
				for(var t=0;t< scheduler.length; t++){	
					var o	= {'id': scheduler[t].__id, 'name': scheduler[t].name, 'last_time': getDateTime(scheduler[t].last_time*1000), 'task': scheduler[t].task}
					_tasks.push(o)
					
				}
				res.render('entity_config_task', {_tasks: _tasks})
			}
		}) 
		return
	}
	else{
		configuration.find({'__type':'scheduled_task'}, function(err, results){
			if(err){
				res.send({'status': 'error'})
				console.log(err)
			}
			else{
				for(var t in results)
					results[t]['_id'] = null
				res.send({'list':results})
				//res.render('entity_config_mtasks', {_mtasks: _mtasks})
			}
		})
	}
}
function getDateTime(milliseconds){
	var d	= new Date(milliseconds)
	var t	= d.getFullYear() + "/"+(d.getMonth() + 1)+"/"+d.getDate()+" "+d.toLocaleTimeString()
	return t;
}

var getData	= function(req, res){
	var contractorsList	= req.query.contractor	
	var id		= req.params.id
	var from	= req.query.from
	if(id){
		if(contractorsList){
			var contractors	= contractorsList.split(",")
			if(from){
				
				data.find({'entity_id': id, 'data' : {$elemMatch: {'name': { $in: contractors}, 'start_time': {$gt : from}}}}, function(err, results){
					if(err)
						console.log(err)
					else {					
						var send = {'data': results}
						res.send(send)
					}
				})
				return
			}
			
			entities.findOne({'entity_id': id}, function(err, result){
				if(err)
					console.log(err)
				else{
					var data	= result.data
					var answer	= {"data": {}}
					for(i in contractors){
						for(var c in data)							
							if(data[c].name	== contractors[i])							
								answer.data[contractors[i]]  = {'time': data[c].start_time, 'value': data[c].result}
							
					}
					res.send(answer)					
				}
			})	
			return			
		}		
		entities.findOne({'entity_id': id}, function(err, result){
			if(err) return error(err, res);
			var data	= result.data
			if(data)
				res.send({'data':data})
		})
	}
}

var test = function(req, res){
	var id 	= req.params.id
	res.render('test_page', {bg_color: 'bg-color-purple'})
}

var agent_GET	= function(req, res){
	var id	= req.params.id
	entities.findOne({'entity_id': id}, function(err, _e){
		if(err) return _error(err, res);
		res.json({'response': _e.agent})		
	})
}
var agent_POST	= function(req, res) {
	var id	= req.params.id
	var files	= req.files
	var result	= {'status': 'error'}
	if(files){
		var file	= files.file
		fs.readFile(file.path, function(err, data){
			if(err) return error(err, res);
			var base64file	= data.toString('base64')
			var upFile	= new collFiles({
				'filename': file.name,
				'chunk': base64file,
				'size': file.size,
				'meta': 0,
				'length': 1,
				'id': String(uuid.v1())
			})
			upFile.save(function(err, _r){
				if(err) return error(err, res)
				groups.find({'agent_id': id}, function(err, _groups){
					if(err) return error(err, res)
					var tags	= []
					for(var i in _groups)
						tags.push(_groups[i].tag)
					var updateCommand = new collCommands({
						'type':	'update',
						'tags': tags,
						'arg': {'id': _r.id}						
					})
					updateCommand.save(function(err, _saved){
						if(err) return error(err, res)
						result.status="ok"					
						res.send(result)
					})
				})
			})
		})
		
		
		
		res.send(result)
	}
}
function tags_GET(req, res){
	var id	= req.params.id
	groups.find({'agent_id':id}, function(err, tags){
		if(err) return error(err, res);
		var data= []
		for(var i in tags){
			data.push(tags[i].tag)
		}
		res.send({'tags': data})
	})
}

exports.init				= init;
exports.group				= entity_group;
exports.entity				= entity_fn;
exports.add_entity			= entity_add;
exports.show_all			= show_allEntities;
exports.upload_contractor	= uploadContractor
exports.get_contractors		= getContractors
exports.setup_scheduler_task= setupTask
exports.manage_tasks		= manageTasks
exports.tasks				= tasks
exports.get_data			= getData
exports.contractors_get		= contractors_get
exports.contractors_post	= contractors_post
exports.test				= test
exports.agent_get			= agent_GET
exports.agent_post			= agent_POST
exports.get_tags			= tags_GET