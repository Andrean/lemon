$(document).ready(function(){

	$( "#page1" ).on('click', function(e){
			$( this ).slideUp(1000);
			$( "div.sidebar" ).animate({'top': '50px'},1000);
			$( document.body ).keypress( function(e){ $( '#page1').slideDown(1000); $( "div.sidebar" ).animate({'top': '170px'},1000); } );
			
		});

});