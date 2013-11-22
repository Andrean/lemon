!function($){
	function getData(container){
		var rel_url 	= '/tags'
		var url			= window.location.toString().match(/^(.+\/inventory\/entities\/[-\w]+)/)[1] + rel_url
		var $container	= $(container)
		var $ul			= $container.find('ul.taglist')
		var $proto		= $ul.find('#prototype')
		$.get(url, function(res){
			for(var i in res.tags){
				var tag = res.tags[i]
				console.log(tag)
				var $li = $proto.clone()
				console.log($li)
				$li.attr('id', 'tag_'+i)
				$li.find('h4').text(tag)
				$li.appendTo($ul)
				$li.show()	
				setHover($li)
			}
		})
	}
	function setHover($li){
		$li.hover(function(){
			$(this).find('.close-anchor').show()
		}, function(){$(this).find('.close-anchor').hide()})
		
	}
	$(document).ready(function(){
		getData('#tags-container')
	})
	
}(window.jQuery)