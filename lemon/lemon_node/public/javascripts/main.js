
$(document).ready(function(){
	var blinkingElements = [];
	var blink = function(){
		for( var el in blinkingElements ){
			$( '#' + blinkingElements[el]).fadeOut(1000);
			$( '#' + blinkingElements[el]).fadeIn(1000);
		}
    };
	setInterval(blink, 2000);
	$( "#page1" ).on('click', function(e){
		$( this ).slideUp(1000);
		$( 'body' ).keypress( function(e){ $( '#page1').slideDown(1000) } );
		
	});
	$.get('/test', function( tiles_json ){
			for( var tile_it in tiles_json )
			{
				var tile	= tiles_json[tile_it];
				var div_tile = $('<div />', {
					'id': 		'tile' + tile.id,
					'class':	 tile['class']
				}).append( $( '<div />' , {
						'class':	tile['subclass']						
					}).append( $('<h6 />').text( tile['agent-short-name'] ))
					  .append( $('<br>'))
					  .append( $('<p />').text("Status: " + tile['agent-status']))
					  .append( $('<p />').text("DNS: " + tile['agent-dns-name']))
					
					)
				  .on('click', function(e){
						$( this ).fadeOut(1000);
						$( this ).fadeIn(1000);
					}
				);
				if( tile['agent-status'] == 'OK')
					div_tile.addClass('bg-color-green');
				if( tile['agent-status'] == 'ERROR'){
					div_tile.addClass('bg-color-red');
					blinkingElements.push('tile' + tile.id);
				}
				if( tile['agent-status'] == 'OVERLOAD'){
					div_tile.addClass('bg-color-orange');
					blinkingElements.push('tile' + tile.id);
				}
							
				$("#servers-box1").append( div_tile );
				//div_tile.clone().attr({'id':'tile' + tile.id +  '_second'}).appendTo($("#servers-box2"));
				
			}
			
		});
	
	
	
});
