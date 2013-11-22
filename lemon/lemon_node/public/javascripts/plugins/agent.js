!function($){
	var template_updateWindow	= "<div class='agent_update_window'><h4 id='name'></h4><h4 id='size'></h4><button id='cancel' class='place-right'>Cancel</button><button id='ok' class='place-right default'>Start updating</button></div>"
	dateFormat.masks.standard	= "yyyy-mm-dd HH:MM:ss"
	function getData(selector){
		var $container	= $(selector)
		var $ul_instances	= $container.find('#instances')
		var $ul_scheduler	= $container.find('#scheduler')
		var rel_url		= '/agent'
		var url			= window.location.toString().match(/^(.+\/inventory\/entities\/[-\w]+)/)[1] + rel_url
		$.get(url, function(res){
			var response	= res.response
			$container.find('.panel-bar > .info').append($('<h4></h4>').text('agent id: ' + response.agent_id))
			$container.find('.panel-bar > .info').append($('<h4></h4>').text("version: "+ response.version))			
			for(var _it in response.scheduler){
				var task	= response.scheduler[_it]
				var li		= $('<li><div class="data"><h4></h4><p></p><p></p></div></li>')
				li.find('.data > h4').text(task.name)
				li.find('.data > p:first').text(task.task.func + " " + ((task.task.args && task.task.args.contractor) || "") )
				li.find('.data > p:last').text(new Date(task.last_time * 1000).format('standard'))
				$ul_scheduler.append(li)
			}
			for(var _it in response.instances){
				var inst	= response.instances[_it]
				var li		= $('<li><div class="data"><h4></h4><p></p></div></li>')
				li.find('.data > h4').text(inst.name)
				li.find('.data > p').text(inst.state)
				$ul_instances.append(li)
			}			
		})		
	}
	function installActions(container){
		var $container	= $(container).parent().parent()
		var $i			= $container.find('form[id="update_agent"] > input[id="i_upload"]')
		$i.on('change', function(e){
			var file 			= this.files[0];
			var form			= $(this).parent()
			var $updateWindow	= $(template_updateWindow)
			var offset			= $container.find('.panel-bar').outerHeight() + $container.find('.panel-header').outerHeight()
			$updateWindow.find('h4:first').text(file.name)
			$updateWindow.find('h4:last').text(file.size + ' bytes')
			$updateWindow.appendTo($container)
			$updateWindow.css('top', offset)
			$updateWindow.slideDown(300)
			$updateWindow.find('button[id="cancel"]').click(function(e){
				e.stopPropagation()
				$updateWindow.slideUp(300, function(){this.remove()})								
			})
			$updateWindow.find('button[id="ok"]').click(function(e){
				e.stopPropagation()
				var $progressBar	= $("<div id='progress'></div>");
				$progressBar.addClass("progress-bar bg-color-darken")
				$progressBar.append($('<div></div>'))
				$progressBar.find('div').addClass("bar bg-color-teal")
				$progressBar.appendTo($updateWindow)
				$updateWindow.find('button').remove()
				var formData = new FormData(form[0]);
				console.log(formData)
				$.ajax({
					url: 'agent',  
					type: 'POST',
					xhr: function() {  
						var myXhr = $.ajaxSettings.xhr();
						if(myXhr.upload){ 
							myXhr.upload.addEventListener('progress',progressState, false); // For handling the progress of the upload
						}
						return myXhr;
					},
					success: completeUpload,
					error: errorUpload,
					data: formData,
					cache: false,
					contentType: false,
					processData: false
				})
				function progressState(e){
					if(e.lengthComputable){
						$progressBar.find('div').width((e.loaded*100 / e.total) + '%')
					}
					
				}
				function completeUpload(e){
					$progressBar.remove()
					$("<div></div>").text('Uploaded').appendTo($updateWindow)
					setTimeout(closePopup,3000)
				}
				function errorUpload(e){
					console.log(e)
				}
				function closePopup(){
					$updateWindow.slideUp(300)
				}
			})
		})
	}	
	function upload($form){
		console.log($form)
		var formData = new FormData($form[0]);
		console.log(formData)
		$.ajax({
			url: 'agent',  
			type: 'POST',
			xhr: function() {  
				var myXhr = $.ajaxSettings.xhr();
				if(myXhr.upload){ 
					myXhr.upload.addEventListener('progress',progressState, false); // For handling the progress of the upload
				}
				return myXhr;
			},
			success: completeUpload,
			error: errorUpload,
			data: formData,
			cache: false,
			contentType: false,
			processData: false
		})
	}	
	function progressState(e){
		if(e.lengthComputable){
			console.log(e)
		}
		
	}
	function completeUpload(e){
		console.log(e)
	}
	function errorUpload(e){
		console.log(e)
	}
	$(document).ready(function(){
		getData('#agent_container')	
		installActions('#agent_container')
		
	})
	
}(window.jQuery)