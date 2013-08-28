(function($){
	function getData(){
		var url	= window.location +'/data?contractor=getProcesses'
		var container	= $("#processes_container")
		var info_block	= container.find('#info_block')
		var ul			= container.find('ul')
		var parent_li	= ul.find('li[id="prototype"]')
		ul.find("li[id^='p_']").detach()
		$.get(url, function(obj){
			var processes = jQuery.parseJSON(obj.data.getProcesses.value)
			processes.time	  = obj.data.getProcesses.time
			var text		= info_block.find('h4[id="process_count"] > b').text()
			info_block.find('h4[id="process_count"] > b').text(text.replace('$', processes.process.length))
			text		= info_block.find('h4[id="stat_time"] > b').text()
			info_block.find('h4[id="stat_time"] > b').text(text.replace('$', (new Date()).format('dd/mm/yyyy HH:MM:ss.L Z',processes.time)))
			for(var _p in processes.process){
				var p	= processes.process[_p]
				var li_item	= parent_li.clone()
				li_item.attr('id','p_'+_p)
				li_item.find('#workingset').text('Working Set: '+formatSize(p.WorkingSet))
				li_item.find('#cpu').text('cpu: '+p.PercentProcessorTime + "%")
				li_item.find('.data > h4').text(p.Name)
				li_item.appendTo(ul)
				li_item.show()
				content	= li_item.find(".process_content")
				content.find("#process_name").text(p.Name)
				content.find("#executable_path").text(p.ExecutablePath)
				content.find("#command_line").text(p.CommandLine)
				content.find("#ProcessId").text(p.ProcessId)
				content.find("#Status").text(p.Status)
				content.find("#ThreadCount").text(p.ThreadCount)
				content.find("#WorkingSetSize").text(p.WorkingSetSize)
				content.find("#WriteOperationCount").text(p.WriteOperationCount)
				content.find("#ReadOperationCount").text(p.ReadOperationCount)
				li_item.click(function(event){
					event.stopPropagation()
					toggleExpand($(this))
				})
			}
		})
	}
	function toggleExpand(line){
		if(line.hasClass('on'))
			line.removeClass('on')
		else
			line.addClass('on')
	}	
	function formatSize(bytes_size){
		bytes_size	= parseFloat(bytes_size)
		if(isNaN(bytes_size))
			return ''
		var suffix	= [' b',' Kb', ' Mb', ' Gb', ' Tb']
		var i	= 0
		while(bytes_size > 1024 && i < suffix.length)
		{
			bytes_size /=1024
			++i
		}
		return bytes_size.toFixed(2) + suffix[i]
	}
	$(document).ready(
		(function(){
			getData()
			setInterval(getData,300000)
		})()
	)
})(window.jQuery)


