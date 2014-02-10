/**
 * 	WebPersonal Services and Functions
 * 
 */
var http		= require('http')
	, fs		= require('fs')
	, mongoose 	= require('mongoose')
	, async		= require('async')
	, ServiceMap= mongoose.model('webpersonal.ServiceMap')
	, Agent		= mongoose.model('system.Agent')
	, History	= mongoose.model('webpersonal.UpdateSession')
	, path		= require('path')
	, subprocess	= require('child_process')
	, _			= require('underscore');

var __prefix__	= 'plugins/';
exports.loadSystems	= function( req, res, next ){
	ServiceMap.load_all( function(err, systems ){
		if(err) return next(err);
		req.wp	= systems || [];
		next();
	});
};

exports.loadServiceMap	= function( req, res, next, name ){
	req.wp.map( function(sys){
		if(sys.info_system == name)
			req.map	= sys;		
	});
	next();
};

exports.main_view	= function( req, res ){	
	History.load( { perPage: 10} ,function( err, list ){
		if(err){ console.log(err); list = []; }
		res.render(__prefix__ + 'webpersonal/webpersonal', { title: 'WebPersonal project', bg_color: 'bg-color-Dark', wp: req.wp, history: list });
	});	
};

exports.view	= function( req, res ){
	var service	= req.params.service || '';
	res.render(__prefix__ + 'webpersonal/webpersonal', 
			{ 	title: 'Update service ' + service,
				wp:	req.wp,
				map:	req.map,
				action: 'update',
				bg_color: 'bg-color-Dark', 
				service: service				
			});
};

exports.upload	= function( req, res ){
	var service	= req.params.service;
	var files	= req.files;
	var status	= {'status':'error'};
	var lemon	= req.app.locals.config.lemon;
	if(files){
		var file	= files.file;
		fs.readFile( file.path, function(err,data){
			if(err){ res.send(status);	return; }
			var headers	= {
					'Content-Disposition': 'attachment;filename='+file.name,
					'Content-Length':file.size,
					'Connection':'close'
			};
			var options	= {
				'hostname': lemon.server.hostname,
				'port': lemon.server.port,
				'path': '/upload',
				'method': 'POST',
				'headers': headers 
			};
			var lemon_req	= http.request(options, function(lemon_res){
				if(lemon_res.statusCode == 201){
					body	= JSON.stringify({ 'info_system':service, 'distr': {'name': file.name }});
					options.path	= '/update/distr';
					options.headers	= {
						'Content-Length': body.length,
						'Content-Type': 'application/json;charset=utf-8',
						'Connection': 'close'
					};
					lemon_res.read();
					lemon_req_2	= http.request( options, function( lemon_res_2 ){
						if(lemon_res_2.statusCode == 200){
							var data 	= '';
							lemon_res_2.on('data', function(chunk){
								data += chunk;
							});
							lemon_res_2.on('end', function(){
								var result	= JSON.parse(data);
								res.send(result);
							});
						}
						else
							res.send(status);
					});
					lemon_req_2.on('error', function(e){
						status.status	= 'error';
						status.msg		= e.message;
						res.send(500,status);				
					});
					lemon_req_2.write(body);
					lemon_req_2.end();
				}
				else{
					status.status	= 'error';
					status.msg		= lemon_res.reason;
					res.send(500,status);
				}
			});
			lemon_req.on('error', function(e){
				status.status	= 'error';
				status.msg		= e.message;
				res.send(500,status);				
			});			
			lemon_req.write(data);
			lemon_req.end();
		});
		return;
	}
	res.send(404, {'status': 'error','msg':'File not found'});
	
};
exports.git_pull= function( req, res ){
	var config	= req.app.locals.config;
	var repo_path	= config.webpersonal.settingsPath;
	var git_path	= config.webpersonal.gitPath || '';
	var env	= _.clone(process.env);
	env.Path += ';'+path.resolve(git_path);
	subprocess.exec(
			'git.exe pull',
			{ cwd: path.resolve(repo_path), env: env }, 
			function(error, stdout, stderr){
				if(error){
					console.log(error);
					res.send('Ошибка: '+ error.Error + '\n' + stderr);
				}
				else
					res.send(stdout);
	});
	
};
exports.setup	= function( req, res ){
	var service		= req.params.service;
	var selected	= req.body.selected;
	var session_id	= req.body.session_id;
	var status		= {'status':'error', 'msg':''};
	var lemon		= req.app.locals.config.lemon;
	if(!selected){
		res.send({});
		return;
	}	
	var body	= JSON.stringify({'services': selected, 'session_id': session_id});
	var headers	= {
		'Content-Length': body.length
	};
	var options	= {
		'hostname': lemon.server.hostname,
		'port': 	lemon.server.port,
		'path': '/update/copy_to_agents',
		'method': 'POST',
		'headers': headers			
	};
	var lemon_req	= http.request(options, function(lemon_res){
		if(lemon_res.statusCode == 200){
			var data 	= '';
			lemon_res.on('data', function(chunk){
				data += chunk;
			});
			lemon_res.on('end', function(){
				var result	= JSON.parse(data);
				if(result.status){
					result.check_link	= '/webpersonal/update/'+service+'/status?link=' + result.check_link;
					res.send(result);
				}
				else
					res.send(status);				
			});
		}
		else
			res.send(status);
	});
	lemon_req.on('error', function(e){
		status.status	= 'error';
		status.msg		= e.message;
		res.send(500,status);				
	});			
	lemon_req.write(body);
	lemon_req.end();
	
};

exports.get_status	= function( req ,res ){
	var link	= req.query.link;
	var status	= {'status':'error','msg':''};
	var lemon	= req.app.locals.config.lemon;
	if(!link){
		res.send();
		return;
	}		
	link	= link.replace(/,/g,'+');
	var options	= {
			'hostname': lemon.server.hostname,
			'port': 	lemon.server.port,
			'path': link,
			'method': 'GET'			
		};
	var lemon_req	= http.request(options, function( lemon_res ){
			if(lemon_res.statusCode == 200){
				var data 	= '';
				lemon_res.on('data', function(chunk){
					data += chunk;
				});
				lemon_res.on('end', function(){
					var result	= JSON.parse(data);
					res.send(result);
				});			
			}
			else
				res.send(500,status);
		});
	lemon_req.on('error', function(e){
		status.status	= 'error';
		status.msg		= e.message;
		res.send(500,status);				
	});	
	lemon_req.end();
};

exports.configure	= function( req, res, next ){
	var service	= req.params.service || '';
	if(service == ''){
		res.render(__prefix__ + 'webpersonal/webpersonal', 
				{	title:'Настройка '+service,
					wp:	req.wp,
					action: 'configure',
					bg_color: 'bg-color-Dark', 
					service: service, 
					map: req.map
				});
		return;
	}
		
	async.map( 
		req.map.map, 
		function(map, callback){			
			Agent.listByTag(map.tag, function(err, agents){
				if(err) return callback(err); 
				map.agents = agents || [];
				callback(null, map);
			});			
		}, 
		function(err, new_map){
			if(err) return next(err);
			req.map.map	= new_map;
			res.render(__prefix__ + 'webpersonal/webpersonal', 
					{	title:'Настройка '+service,
						wp:	req.wp,
						action: 'configure', 
						bg_color: 'bg-color-Dark', 
						service: service, 
						map: req.map
					});
		}
	);
		
};

exports.edit_system_map	= function(req, res){
	for(var key in req.body)
		req.map[key]	= req.body[key];
	req.map.save(function(err){
		if(err){ console.log(err);res.send(500);return;	}
		res.send();
	});
};

exports.edit_map	= function( req, res ){	
	req.body.services.map(function(srv,i,arr){
		req.map.services.forEach(function(el){
			if(el.name == srv){
				arr[i]	 = { name: srv, settings: []};
				el.settings.map(function(setting){
					arr[i].settings.push({ name: setting, fileName: setting});
				});
			}
		});		
	});
	req.map.map.push(req.body);
	req.map.save(function(err, data){
		if(err) return next(err);
		res.send({});
	});	
};

exports.del_map	= function(req, res){
	var tag	= req.query.tag;
	var remove = '';
	for(var i in req.map.map){
		var item	= req.map.map[i];
		if(item.tag == tag)
			remove = i;
	}
	req.map.map.splice(remove,1);
	req.map.save(function(err){
		if(err){ console.log(err); res.send(500); return;}
		res.send();
	});
};
exports.load_settingsList	= function( req, res, next ){
	var service	= req.params.service;
	/*fs.readdir(req.app.locals.config.webpersonal.settingsPath + '/' + service + '/settings', function( err, files ){
		req.map.settings = {errmsg: ''};
		if(err){ console.log(err); req.map.settings.errmsg = "Не удалось получить список файлов"; }  
		req.map.settings.files = files;	
		
		next();
	});*/
};
exports.services	= function( req, res ){
	var service	= req.params.service || '';
	res.render(__prefix__ + 'webpersonal/webpersonal', 
			{	title:		'Настройка службы '+service,
				wp:			req.wp,
				action: 	'configure_services',
				bg_color: 	'bg-color-Dark', 
				service: 	service, 
				map: 		req.map 
			});
};
exports.edit_services	= function( req, res ){
	req.map.services.push(req.body);
	req.map.save(function(err, data){
		if(err){ console.log(err); res.send(500);return;};
		res.send({});
	});
};

exports.switch_services	= function( req, res ){
	var session_id	= req.body.session_id;
	lemon_switchrequest('/update/switch_services', req, res, session_id);
};
exports.switch_fronts	= function( req, res ){
	var session_id	= req.body.session_id;
	lemon_switchrequest('/update/switch_fronts', req, res, session_id);
};
function lemon_switchrequest(path, req, res, session_id){
	var lemon		= req.app.locals.config.lemon;
	var status	= {'status':'error',msg:''};
	var body	= JSON.stringify({'session_id': session_id});
	var headers	= {
		'Content-Length': body.length
	};
	
	l_opts	= {
			'hostname': lemon.server.hostname,
			'port': 	lemon.server.port,
			'path': path,
			'method': 'POST',
			'headers': headers			
		};
	var l_req	= http.request(l_opts, function(l_res){
		if(l_res.statusCode == 200){
			var data 	= '';
			l_res.on('data', function(chunk){
				data += chunk;
			});
			l_res.on('end', function(){
				var result	= JSON.parse(data);
				if(result.status){
					result.check_link	= '/webpersonal/update/'+req.params.service+'/status?link=' + result.check_link;
					res.send(result);
				}
				else
					res.send(status);				
			});
		}
		else
			res.send(status);
	});
	l_req.on('error', function(e){
		status.status	= 'error';
		status.msg		= e.message;
		res.send(500,status);				
	});			
	l_req.write(body);
	l_req.end();	
}
exports.projects_new	= function( req, res ){
	ServiceMap.create(req.body, function(err, system){
		if(err){ res.send(500); console.log(err); return;}
		res.send(system);
	});
};

exports.get_history		= function( req, res ){
	History.load(function( err, list ){
		async.map(
			list,
			function(el, cb){
				if(el.info_system == req.params.service || !req.params.service)
					cb(null, el);
			},
			function(err, selected_list){
				if(err){ res.send({}); return; }
				res.send(selected_list || []);
			}
		);
	});	
};