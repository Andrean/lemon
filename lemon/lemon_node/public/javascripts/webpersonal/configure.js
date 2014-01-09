!function($){	
	$('#wrap_add_servicegroup').find('#submit').on('click', function(){
		var formData	= $('#form_add_servicegroup').serializeObject();
		console.log(formData);
		$.ajax({
			url: $('#form_add_servicegroup').attr('action'),
			type: 'POST',
			data: formData,
			success: function(data){
				location.reload();
			},
			error:	 function(data){}
		});
	});
	$('button[data-action="select_add_agent"]').click(function(){
		var $this	= $(this);
		var $target	= $($this.attr('data-target'));
		var tag		= $this.attr('tag');
		$.ajax({
			url:	'/agents?exclude='+tag,
			type:	'GET',
			success:	function(data){
				var $select = $target.find('select');
				$select.children().detach();
				for(var i in data.excluded){
					var agent	= data.excluded[i];
					$select.append($('<option></option>').val(agent.agent_id).text(agent.name || agent.agent_id));
				}				
			},			
		});		
	});
	$(document).on('click', 'button[data-action="add_agent"]', function(){
		var $this	= $(this);
		var tag		= $this.attr('tag');
		var $target	= $this.parent().find('select');
		var agent_ids	= $target.val();
		var agents	= [];
		for(var i in agent_ids){			
			agents.push( { agent_id: agent_ids[i], tags: [tag]} );
		}
		console.log(agents);
		$.ajax({
			url:	'/agents',
			type:	'POST',
			data:	{ agents: agents },
			success: function(data){
				location.reload();
			}
		});
	});
	$('div[data-role="copy"]').on('click', function(){
		var $this	= $(this);
		var $parent = $this.parents($this.attr('data-copy'));
		$new_parent = $parent.clone();
		$new_parent.find('div[data-role="copy"]').removeClass('icon-plus-2').addClass('icon-minus-2').on('click',function(){
						$(this).parents($this.attr('data-copy')).remove();
					});
		$new_parent.find('input').val('');
		$new_parent.appendTo($parent.parent());
	});
	
	$('#wrap_add_service').find('#submit').on('click', function(){
		var url	= $('#form_add_service').attr('action');
		var formData	= $('#form_add_service').serializeObject();
		$.ajax({
			url:	url,
			type:	'POST',
			data:	formData,
			success: function(data){
				location.reload();
			}			
		});
	});
	$('button[data-action="showinput"]').on('click',function(){
		var $input	= $(this).parent().children('input');
		$input.show();
		$(this).text('Сохранить');
		$(this).on('click', function(){
			var value	= $input.val();
			var name	= $input.attr('name');
			var data	= {}; data[name] = value;
			$.ajax({
				url: location + '/system',
				type: 'POST',
				data: data,
				success: function(data){
					location.reload();
				},
			});			
		});
	});
	$('button[data-action="delete_map"]').on('click', function(){
		var tag	= $(this).attr('tag');
		$.ajax({
			url: location+'/map?tag='+tag,
			type: 'DELETE',
			success: function(){
				location.reload();
			}
		});
	});
}(window.jQuery);