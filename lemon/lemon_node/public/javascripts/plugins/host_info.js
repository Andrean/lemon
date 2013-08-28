(function($){
	function getData(){
		url	= window.location + '/data?contractor=getHostInfo'
		$.get(url, function(result){
			console.log(result)
			var obj	= jQuery.parseJSON(result.data.getHostInfo.value)
			var cs	= obj.computersystem[0]
			var status	= 'OK'
			$.get(window.location+'?time=1', function(res){
				var t = new Date()
				var diff	= t.getTime() - res.time*1000
				t.setTime(res.time*1000)
				var msg	= t.getFullYear() + "/" + (t.getMonth()+1) + "/" +t.getDate() + " " + t.getHours() + ":" + t.getMinutes() + ":" + t.getSeconds() + "." + t.getMilliseconds()
				$('#e_lastcheck').text(msg)
				console.log(diff)
				if(diff > 300000)
					status = 'NOT ANSWERED'
				if(status	== 'OK')
					status	= cs.Status
				$('#e_hoststatus').text(status)
				if(status	 == 'OK'){
						$('#e_hoststatus').parent().removeClass('error')
						$('#e_hoststatus').parent().addClass('success')
					}
				else{
					$('#e_hoststatus').parent().removeClass('success')
					$('#e_hoststatus').parent().addClass('error')
					}
			})
			$('#e_name').text(cs.Caption)
			$('#e_os').text(obj.os[0].Caption)
			$('#e_os_version').text(obj.os[0].Version)
			if(obj.computersystem[0].Domain)
				$('#e_dnshostname').text(cs.Domain + '\\' + obj.computersystem[0].DNSHostName)
			else
				$('#e_dnshostname').text(cs.DNSHostName)
			$('#e_manufacturer').text(cs.Manufacturer)
			$('#e_model').text(cs.Model)
			$('#e_num_of_cpu').text(cs.NumberOfLogicalProcessors)
			$('#e_num_of_physical_cpu').text(cs.NumberOfProcessors)
			var cpu	= obj.cpu[0]
			$('#cpu_manufacturer').text(cpu.Manufacturer)
			$('#cpu_name').text(cpu.Name)
			$('#cpu_maxclockspeed').text(cpu.MaxClockSpeed + " MHz")
			$('#cpu_currentclockspeed').text(cpu.CurrentClockSpeed + " MHz")
			$('#cpu_description').text(cpu.Description)
			//if(obj.cs.Caption){
			//	$('head > title').text(obj.cs.Caption + " information page")
			//	$('#entity_header > h3').text(obj.cs.Caption + " information")
			//}
			
		})
	}
	$(document).ready(
		function(){
			getData()
			setInterval(getData, 30000)
		}
	)	
})(window.jQuery)