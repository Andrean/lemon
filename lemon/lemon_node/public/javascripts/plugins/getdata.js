!function($){
	function getData(contractors){
		var rel_url		= '/data'
		if(contractors)	rel_url += "?contractor=" + contractors.join(',')
		var url			= window.location.toString().match(/^(.+\/inventory\/entities\/[-\w]+)/)[1] + rel_url
		$.get(url, function(res){
			var data	= res.data
			localStorage.setItem('data', JSON.stringify(data))
		})		
	}
	
	$(document).ready(function(){
		var contractors	= ['getSystemInfo']
		getData(contractors)
		setInterval(function(){	getData(contractors)	}, 5000)
	})
	
}(window.jQuery)