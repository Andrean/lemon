(function($){
	dateFormat.masks.standard	= "yyyy-mm-dd HH:MM:ss"
	var states	= ['init','running','stopped']
	function getData(){
		var rel_url		= '/contractors'
		var url			= window.location.toString().match(/^(.+\/inventory\/entities\/[-\w]+)/)[1] + rel_url
		var $container	= $('#contractors_container')
		var $ul			= $container.find('ul')
		var $prototype	= $ul.find('li[id="__prototype"]')
		$ul.find('li[id^="c_"]').detach()
		$.get(url, function(_list){
			var list = _list.response
			localStorage.setItem('contractors', JSON.stringify(list))
			for(var _i in list){
				var contractor	= list[_i]
				var li_item		= $prototype.clone()
				li_item.attr('id','c_' + _i)
				li_item.find('.data > h4').text(contractor.name)
				li_item.find('.data > #size').text(formatSize(contractor.size))
				if(contractor.enabled)
					li_item.find('.status').addClass('icon-checkmark').addClass('fg-color-green')
				else
					li_item.find('.status').addClass('icon-cancel-2').addClass('fg-color-orange')
				li_item.find('.status')
				li_item.appendTo($ul)
				li_item.show()
				if(contractor.enabled)
					li_item.find('.c-commands').find('#btn_enable').hide()
				else
					li_item.find('.c-commands').find('#btn_disable').hide()
				li_item.find('.c-commands').attr('id', 'cc__' + li_item.attr('id'))
				li_item.find('.c-commands').find('#btn_update').click(function(e){
					e.stopPropagation()
					showModal($container, 'update', $(this))
				})
				li_item.find('.c-commands').find('#btn_delete').click(function(e){
					e.stopPropagation()
					btnAction('delete', $container, $(this))
				})
				li_item.find('.c-commands').find('#btn_enable').click(function(e){
					btnAction('enable', $container, $(this))
				})
				li_item.find('.c-commands').find('#btn_disable').click(function(e){
					btnAction('disable', $container, $(this))
				})
				li_item.click(function(e){
					clickHandler(e, $(this), $(this).find('.c-commands'),list)
				})
			}
		})
	}
	function clickPanelBox(container){
		var panel	= container.parents('.panel')
		var input_add	= panel.find('#i_upload')
		input_add.on('change', function(e){
			var file = this.files[0];
			var parent = $(this).parent().parent()
			var formData = new FormData(parent[0]);
			
			$.ajax({
				url: '/inventory/entities/contractors',  //Server script to process data
				type: 'POST',				
				success: getData,
				data: formData,
				cache: false,
				contentType: false,
				processData: false
			});			
		})
	}
	function formatSize(bytes_size){
		bytes_size	= parseFloat(bytes_size)
		if(isNaN(bytes_size))
			return ''
		var suffix	= [' b',' Kb', ' Mb', ' Gb', ' Tb']
		var i	= 0
		while(bytes_size > 1024 && i < suffix.length-1)
		{
			bytes_size /=1024
			++i
		}
		if(i < 1)
			return bytes_size.toFixed(0) + suffix[i]
		return bytes_size.toFixed(2) + suffix[i]
	}
	function selectItem(item){
		if(!item.hasClass('c-selected')){
			item.addClass('c-selected')
			return true
		}
		item.removeClass('c-selected')
		return false
	}
	function clickHandler(e, root, item, _c){
		e.stopPropagation()
		if(!root.hasClass('c-selected'))
		{
			var parent 	= root.parent()
			var prev	= parent.find('.c-selected')
			prev.trigger('click')
		}
		var flag	= selectItem(root)
		toggleWindow(root, item, flag, _c)
	}
	function toggleWindow(root, item, turn, _c){
		if(turn){
			var delta	= 14
			var offset 	= root.offset()
			var it		= root.attr('id').match(/^c_(\w+)/)[1]
			var c		= _c[it]
			item.css('top',offset.top)
			item.css('left', offset.left + root.outerWidth() + delta)
			item.appendTo($('body'))
			item.find('.c-header > h4').text(c.name)
			item.find("#size").text(c.size + ' bytes')
			item.find("#rev").text(c.revision)
			item.find("#tags").text(c.tags)
			if(c.data){
				item.find("#start_time").text(new Date(c.data.start_time * 1000).format('standard'))
				item.find("#duration").text((c.data.duration_time || 0).toFixed(3) + " seconds")
				item.find("#state").text(states[c.data.state || 0])
				}
			else{
				item.find("#start_time").text(" - ")
				item.find("#duration").text(" - ")
				item.find("#state").text(" - ")
			}
			item.show()
			root.unbind('click')
			root.click(function(e){ 
				clickHandler(e, root, item, _c)	
			})
		}
		else{
			item.hide()
			root.unbind('click')
			root.click(function(e){				
				clickHandler(e, root, item, _c)		
			})
		}
	}
	function btnAction(action, container, item)	{
		if(action == 'delete')
		{
			_delete(container, item)
			return
		}
		if(action == 'enable')
			_toggle(true, container, item)
		if(action == 'disable')
			_toggle(false, container, item)
	}
	function _toggle(cmd, container, item){
		console.log("performed toggle action")
		var url	= '/inventory/entities/contractors'
		var parent 	= item.parents(".c-commands")
		var id 		= parent.attr('id')
		var li_id	= id.match(/^cc__([\w_]+)/)[1]
		var name 	= container.find('#'+li_id).find('.data > h4').text()
		$.post(url, {'change': true, 'enable': cmd, 'name': name}, function(res){
			container.find('#'+li_id).trigger('click')
			if(res.status == 'ok')				
				getData()
		})		
	}
	function _delete(container, item){
		var deleteURL	= '/inventory/entities/contractors'
		var parent 	= item.parents(".c-commands")
		var id 		= parent.attr('id')
		var li_id	= id.match(/^cc__([\w_]+)/)[1]
		var name 	= container.find('#'+li_id).find('.data > h4').text()
		$.post(deleteURL, {'delete': true, 'name': name}, function(res){
			if(res.deleted)
				container.find('#'+li_id).trigger('click').detach()
				getData()
		})
	}
	
	

	$(document).ready(
		function(){
			getData()	
			clickPanelBox($('#contractors_container'))
			$(document).tooltip({
				selector:"input[data-toggle='tooltip'],div[data-toggle='tooltip'],button[data-toggle='tooltip']", 
				container: 'body',
				animation: true,
				delay: {show: 200, hide: 100}
			})
			$("#myModal").modal({'show': false})
		}
		
	)
	function showModal(container, sItem, item){
		var id 		= sItem + '_modal'
		var modal	= container.find('#'+id)
		var ccomands	= item.parents('.c-commands')
		var name	= ccomands.find('.c-header > h4').text()
		modal.attr('id', id + '__parent__'+container.attr('id'))
		console.log(name)
		modal.attr('contractor_name', name)
		modal.appendTo($('body')).css('top','30%').fadeIn(150)
		var back 	= $("#backdrop")
		back.appendTo($('body'))
		back.show()
		modal.find('.close').click(function(e){e.stopPropagation(); hideModal(modal)})
		modal.find('.modal-header > h3').text('Update')
		modal.find('.modal-body > p').detach()
		modal.find('#dropbox').show()
		
	}
	function hideModal(modal){
		var ids		= modal.attr('id')
		var id		= ids.match(/([\w_]+)__parent__([\w_]+)/)
		modal.fadeOut(150)
		modal.css('top','-45%')
		modal.appendTo($('#'+id[2]))
		modal.attr('id',id[1])
		modal.attr('contractor_name','')
		modal.find('.close').unbind('click')
		$("#backdrop").hide()
	}	
})(window.jQuery)