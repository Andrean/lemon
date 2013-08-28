(function($){
	function getData(){
		var url	= window.location +'/data?contractor=getDiskInfo'
		var container	= $("#disk_container")
		var ul			= container.find('ul')
		var parent_li	= ul.find('li[id="d_prototype"]')
		ul.find("li[id^='disk_']").detach()
		$.get(url, function(obj){
			var disks = jQuery.parseJSON(obj.data.getDiskInfo.value)
			disks.time	= obj.data.getDiskInfo.time
			ul.find("#loader").hide()
			for(var _d in disks.logicaldisk){
				var d 	= disks.logicaldisk[_d]
				var li_item	= parent_li.clone()
				li_item.attr('id',"disk_"+_d)
				li_item.find('#Name').text(d.VolumeName + "("+d.Name+")")
				li_item.find('#Description').text(d.Description)
				if(d.DriveType != 5 )
					li_item.find('#Size').text(formatSize(d.FreeSpace) + " free of " + formatSize(d.Size))
				li_item.find('#bar_freespace').css('width',((d.FreeSpace / d.Size)*100) + '%')
				li_item.find('.icon').append($('<img src="'+getDriveType(d.DriveType)+'"/>'))
				li_item.show()
				li_item.appendTo(ul)
			}
		})
		
	}
	function getDriveType(num){
		var root	= '/images/drives/'
		var file	= ['unknown.png', 'norootdir.png','removable.png','hdd.png','nethdd.png','dvd.png','ram.png']
		num	= num % file.length
		return root + file[num]
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
	$(document).ready(function(){
		getData()
		setInterval(getData, 30000)
	})

})(window.jQuery)