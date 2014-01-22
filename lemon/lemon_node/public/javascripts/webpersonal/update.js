!function($){
	var session_id	= '';
	var status	= ['present','submit','pending','completed','error'];
	status[-1]	= 'error';
	$('#upload_form > div > input').on('change', function(){
		distr_file	= this.files[0].name;
		var parent = $(this).parent().parent();
		var formData = new FormData(parent[0]);		
		enable_loader($('#upload_form > div'));
		$('#console').remove();
		$('#update_instruction').remove();
		$.ajax({
			url: $('#upload_form').attr('action'), 
			type: 'POST',				
			success: function(data){
				disable_loader($('#upload_form > div'));
				$('#upload_form > div').text('Загружено').removeClass('default').addClass('success');
				if(data.status){
					var services	= data.data;
					session_id		= data.session_id;
					var $ul	= $('<div id="service_list" class="listview small" style="margin-left:0"></div>');
					$ul.appendTo($('.lemon-container'));
					for(var i in services){
						var srv	= services[i];						
						var $a	= $('<a class="list shadow"></a>');
						$a.append(
								$('<div class="list-content"></div>')
									.append($('<span class="icon icon-checkbox-unchecked"></span><div class="data"><span class="list-title"></span></div>'))
						);
						$a.attr('service_name',srv.service);
						$a.find('.list-title').text(srv.service);
						$a.click(function(){
							if(!$(this).hasClass('selected')){
								$(this).addClass('selected');
								$(this).find('.icon-checkbox-unchecked').removeClass('icon-checkbox-unchecked').addClass('icon-checkbox');
								return;
							}
							$(this).removeClass('selected');
							$(this).find('.icon-checkbox').addClass('icon-checkbox-unchecked').removeClass('icon-checkbox');
						});
						$ul.append($a);
					}
					var $setupButton	= $('#setup_copy');
					$setupButton.addClass('default');
					$setupButton.click(function(){ setup_copy(this); });
				}				
			},
			error: function(data){
				$('#upload_form > div').text('Ошибка').removeClass('default').addClass('danger');				
			},
			data: formData,
			cache: false,
			contentType: false,
			processData: false
		});		
	});
	
	function enable_loader($btn){
		$btn.contents().filter(function(){ return this.nodeType == 3; }).remove();;
		$btn.append($('<img src="/images/76.gif" class="line-loader">'));
	}
	function disable_loader($btn){
		$btn.find('img').remove();		
	}
	function setup_copy(btn){
		var $checked = $('.lemon-container > #service_list').find('.selected');
		var data	= { 'selected': [], 'session_id':session_id };
		var btn_id	= $(btn).attr('id');
		$checked.each(function(){
			data.selected.push($(this).attr('service_name'));
		});
		$('.lemon-container > #service_list').remove();
		enable_loader($(btn));
		var $url	= window.location + '/setup';
		$.ajax({
			url: $url,
			type: 'POST',
			data: data,
			success: function(data){
				if(data.status){					
					setTimeout(function(){ check_status(data.check_link, data.tags, btn_id) ;} , 500);				}
			},
			error: function(data){ disable_loader($(btn)); $(btn).text('Ошибка').addClass('danger').removeClass('default');console.log('error'); console.log(data);}
		});
	}
	function get_agents(tags, cb){
		if(!tags){
			cb();
			return;
		}
		var $ul	= $('.lemon-container').children('.listview');
		if($ul.length == 0){
			$ul	= $('<div class="listview small" style="margin-left:0"></div>');
			$ul.appendTo($('.lemon-container'));
		}
		$.get('/agents?tag='+tags.join(','), function(data){
			var agents	= data.data;
			agents.map( function(agent){
				var $a	= $('<a class="list bg-darkBlue fg-white"></a>');
				$a.append(
						$('<div class="list-content"></div>')
							.append($('<span class="icon icon-windows"></span><div class="data"><span class="list-title"></span></div>'))
				);
				$a.attr('agent_id',agent.agent_id);
				$a.find('.list-title').text(agent.name);
				$ul.append($a);
			});
			cb();
		});
	}
	function check_status(link, tags, btn){
		get_agents(tags, function(){
			$.get(link, function( data ){
				console.log(data);
				var $ul	= $('.lemon-container').children('.listview');							
				for(var i in data){
					var command = data[i];
					for(var item_i in command){
						var item	= command[item_i];
						var $a	=	$ul.children('a[agent_id='+item.agent_id+']');
						if($a.find('span[cmd_id='+i+']').length == 0)
							$a.find('.data').append($('<span cmd_id="'+i+'" class="list-remark"></span>'));						
						$a.find('span[cmd_id='+i+']').text(status[item.status]);										
					}
				}							
			});	
		});
		var completed = true;
		if($('.lemon-container').children('.listview').find('a').length == 0)
			completed = false;
		$('.lemon-container').children('.listview').find('a').each(function(){
			var $agent_item	= $(this);
			if($agent_item.find('.list-remark').length == 0)
				completed = false;
			$agent_item.find('.list-remark').each(function(){
				if($(this).text() != 'completed' && $(this).text() != 'error')
					completed = false;
			});	
		});
		if(completed){
			copy_completed(null, btn);
			return;
		}
		setTimeout( function(){ check_status(link, null, btn); }, 500);
	}
	function copy_completed(err, btn){
		var $btn	= $('#' + btn);
		disable_loader($btn);
		if(err)
			$('.lemon-container').find('#' + btn).text('Ошибка').removeClass('default').addClass('danger');
		$('.lemon-container').find('#' + btn).text('Готово').removeClass('default').addClass('success');
		var $switch_services	= $('.lemon-container').find('#switch_services');
		if(!$switch_services.hasClass('default') && !$switch_services.hasClass('success'))
			$switch_services
				.on('click',function(){ switch_services(this); })
				.addClass('default');
		var $switch_fronts	= $('.lemon-container').find('#switch_fronts');
		if(!$switch_fronts.hasClass('default') && !$switch_fronts.hasClass('success'))
			$switch_fronts
				.on('click',function(){ switch_fronts(this); })
				.addClass('default');
		
	}
	function switch_services(btn){
		var $this	= $(btn);
		$this.off();
		enable_loader($this);
		$.ajax({
			url: location +'/switch_services',
			type: 'POST',
			data: {'session_id': session_id},
			success: function(data){
				if(data.status != 'error'){
					$('.lemon-container').children('.listview').remove();
					setTimeout(function(){ check_status(data.check_link, data.tags, $this.attr('id')) ;} , 500);
				}
				else{
					disable_loader($this);
					$this.addClass('danger').removeClass('default').text('Ошибка');
				}
			},
			error: function(error){
				disable_loader($this);
				console.log(error);
			}
		});
	}
	
	function switch_fronts(btn){		
		var $this	= $(btn);
		$this.off();
		enable_loader($this);
		$.ajax({
			url: location +'/switch_fronts',
			type: 'POST',
			data: {'session_id': session_id},
			success: function(data){
				if(data.status != 'error'){
					$('.lemon-container').children('.listview').remove();
					setTimeout(function(){ check_status(data.check_link, data.tags, $this.attr('id')) ;} , 500);
				}
				else{
					disable_loader($this);
					$this.addClass('danger').removeClass('default').text('Ошибка');
				}
			},
			error: function(error){
				disable_loader($this);
				console.log(error);
			}
		});
	}
	
	$(document).ready( function(){
		$.get('/webpersonal/settings/pull',function(data){
			$('#console').remove();
			$('.lemon-container').append($('<textarea id="console" cols="60" rows="4">').text("Executing git pull...\n"+data));
		});
	});
}(window.jQuery);