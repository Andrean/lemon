!function($){
	var distr_file	= '';
	var session_id	= '';
	var status	= ['present','submit','pending','completed','error'];
	$('#upload_form > div > input').on('change', function(){
		distr_file	= this.files[0].name;
		var parent = $(this).parent().parent();
		var formData = new FormData(parent[0]);		
		$('#upload_form > div').text('Загрузка').append($('<img src="/images/loader.gif"/>'));
		$.ajax({
			url: $('#upload_form').attr('action'), 
			type: 'POST',				
			success: function(data){
				$('#upload_form > div').text('Загружено').removeClass('default').addClass('success');
				if(data.status){
					var services	= data.data;
					session_id		= data.session_id;
					for(var i in services){
						var srv	= services[i];
						var $check	= $('<input type="checkbox">');
						var $wrap	= $('<div class="input-control checkbox"><label></label></div>');
						var $label	= $wrap.find('label');
						$check.prop('name', srv.service);
						$check.prop('id','service_'+srv.service);
						$check.val(srv.service);
						$check.prop('checked','checked');
						$label.text(srv.service);
						$label.append($check);
						$label.append($('<span class="check"></span>;'));
						$wrap.appendTo($('.lemon-container'));
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
	
	function setup_copy(btn){
		var $checked = $('.lemon-container').find('input:checkbox:checked');
		var data	= { 'selected': [], 'session_id':session_id };
		$checked.each(function(){
			data.selected.push($(this).val());
		});
		$('.lemon-container').find('label').remove();
		$(btn).text('Установка');
		var $url	= window.location + '/setup';
		$.ajax({
			url: $url,
			type: 'POST',
			data: data,
			success: function(data){				
				if(data.status){
					console.log(data);
					setTimeout(function(){ check_status(data.check_link) ;} , 500);
				}
			},
			error: function(data){console.log('error'); console.log(data);}
		});
	}
	
	function check_status(link){
		$.get(link, function( data ){
			console.log(data);
			var $ul	= $('.lemon-container').children('.listview');
			if($ul.length == 0){
				$ul	= $('<div class="listview small" style="margin-left:0"></div>');
				$ul.appendTo($('.lemon-container'));
			}			
			for(var i in data){
				var command = data[i];
				for(var item_i in command){
					var item	= command[item_i];
					$a	=	$ul.children('a[agent_id='+(item.name || item.agent_id)+']'); 
					if($a.length == 0){
						$a	= $('<a class="list bg-darkBlue fg-white"></a>');
						$a.append(
								$('<div class="list-content"></div>')
									.append($('<span class="icon icon-windows"></span><div class="data"><span class="list-title"></span></div>'))
						);
						$a.attr('agent_id',item.agent_id);
						$a.find('.list-title').text(item.agent_id);
						$ul.append($a);
					}					
					if($a.find('span[cmd_id='+i+']').length == 0)
						$a.find('.data').append($('<span cmd_id="'+i+'" class="list-remark"></span>'));						
					$a.find('span[cmd_id='+i+']').text(status[item.status]);										
				}
			}			
			
		});	
		var completed = true;
		if($('.lemon-container').children('.listview').find('a').length == 0)
			completed = false;
		$('.lemon-container').children('.listview').find('a').each(function(){
			var $agent_item	= $(this);
			$agent_item.find('.list-remark').each(function(){
				if($(this).text() != 'completed' && $(this).text() != 'error')
					completed = false;
			});			
			
		});
		if(completed){
			copy_completed();
			return;
		}
		setTimeout( function(){ check_status(link); }, 500);
	}
	function copy_completed(err){
		if(err)
			$('.lemon-container').find('#setup_copy').text('Ошибка').removeClass('default').addClass('danget');
		$('.lemon-container').find('#setup_copy').text('Скопировано').removeClass('default').addClass('success');
		var $switch_services	= $('.lemon-container').find('#switch_services').addClass('default');
		$switch_services.on('click', function(){ switch_services(this); });
		var $switch_fronts	= $('.lemon-container').find('#switch_fronts').addClass('default');
		$switch_fronts.on('click', function(){ switch_fronts(this); });
	}
	function switch_services(btn){
		var $this	= $(btn);
		$.ajax({
			url: location +'/switch_services',
			type: 'POST',
			data: {'session_id': session_id},
			success: function(data){
				if(data.status){
					console.log(data);
					$('.lemon-container').children('.listview').remove();
					setTimeout(function(){ check_status(data.check_link) ;} , 500);
				}
			},
			error: function(error){
				console.log(error);
			}
		});
	}
	
	function switch_fronts(btn){
		var $this	= $(btn);
		$.ajax({
			url: location +'/switch_fronts',
			type: 'POST',
			data: {'session_id': session_id},
			success: function(data){
				if(data.status){
					console.log(data);
					$('.lemon-container').children('.listview').remove();
					setTimeout(function(){ check_status(data.check_link) ;} , 500);
				}
			},
			error: function(error){
				console.log(error);
			}
		});
	}
}(window.jQuery);