
$(document).ready(function(){
	function installTile(selector){
		parent	= selector.parent().parent().parent()
		id	= (parent.attr('id')).match(/entity_tile([\w\-]+)/)[1]
		url	= "/inventory/entities/" + id+"?install=1"
		$.get(url, function(result){
			console.log(result.status)
			if(result.status == 'ok')
			{
				parent.appendTo($('#default_group > div.group-content'))
				parent.find("#btn_install").hide()
				parent.find("#btn_delete").hide()
				parent.find("#btn_uninstall").show()
			}
		})
	}
	function removeTile(selector){
		parent	= selector.parent().parent().parent()
		id	= (parent.attr('id')).match(/entity_tile([\w\-]+)/)[1]
		url	= "/inventory/entities/"+id+"?delete=1"
		$.get(url, function(result){
			console.log(result.status)
			if(result.status == 'removed')
				parent.remove()
		})
	}
	function uninstallTile(selector){
		parent	= selector.parent().parent().parent()
		id	= (parent.attr('id')).match(/entity_tile([\w\-]+)/)[1]
		console.log(id)
		url	= "/inventory/entities/"+id+"?install=2"
		console.log(url)
		$.get(url, function(result){
			console.log(result)
			if(result.status == 'ok')
			{
				parent.appendTo($('#trash > div.group-content'))
				parent.find("#btn_install").show()
				parent.find("#btn_delete").show()
				parent.find("#btn_uninstall").hide()
			}
		})
	}
	function showModal(selector, action, element){
		$("#backdrop").show()
		selector.show()
		selector.animate({'top':'10%'},100)			
		$( "#confirm").find("button.close").click(function(e){
		e.stopPropagation()
			hideModal($("#confirm"))
		})
		$("#confirm").find("#modal_cancel").click(function(e){
			hideModal($("#confirm"))
		})
		$("#confirm").find("#modal_ok").click(function(e){
			hideModal($("#confirm"))
			action(element)
		})
	}
	function hideModal(selector){
		$("#backdrop").hide(100)
		selector.animate({'top':'-45%'},200)
		selector.hide(300)		
	}	
	
	
	$( "div[id^=entity_tile]" ).on('click', function(e){
		var entity_id = $(this).attr('id');
		entity_id = entity_id.substr(11);
		window.open('/inventory/entities/'+entity_id);
		
	});
	$( ".group-content" ).find("div[id^=entity_tile]" ).hover(
		function(e){
			$(this).find('div.command-line').fadeIn(200)
		},
		function(e){
			$(this).find('div.command-line').fadeOut(100);
		}
	)
	
	$( "div[id^=entity_tile] > div > div > button[id='btn_delete']" ).click(function(event){
		event.stopPropagation()
		showModal($('#confirm'),removeTile, $(this))		
	})
	$( "div[id^=entity_tile] > div > div > button[id='btn_install']" ).click(function(event){
		event.stopPropagation()
		showModal($('#confirm'),installTile, $(this))		
	})
	$( "div[id^=entity_tile]").find("button[id='btn_uninstall']" ).click(function(event){
		event.stopPropagation()
		showModal($('#confirm'),uninstallTile, $(this))
	})
	
	
});
