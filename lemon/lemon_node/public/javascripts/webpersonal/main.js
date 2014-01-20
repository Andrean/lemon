!function($){
	$('#new_project').click( function(){
		$('#form_new_project').show();
	});
	
	$('#form_new_project').find('#submit').click(function(){
		var $form	= $('#form_new_project > form');
		var url		= $form.attr('action');
		var method	= $form.attr('method');
		var data	= $form.serializeObject();
		$.ajax({
			url: url,
			type: method,
			data: data,
			success: function(res){
				location.assign('/webpersonal/configure/'+res.info_system);
			},
			error: function(){
				var $alert	= $('<div class="popup-alert">Ошибка</div>').hide(); 
				$form.append($alert);
				$alert.slideDown(300);
			}
		});
	});
}(window.jQuery);
