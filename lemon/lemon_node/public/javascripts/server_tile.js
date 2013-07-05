
$(document).ready(function(){
	
	$( "div[id^=entity_tile]" ).on('click', function(e){
		var entity_id = $(this).attr('id');
		entity_id = entity_id.substr(11);
		window.open('/inventory/entities/'+entity_id);
		
	});
	
	
	
	
});
