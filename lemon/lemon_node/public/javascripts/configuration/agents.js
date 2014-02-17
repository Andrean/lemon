/**
 *  	/configuration/agents.js client script 
 */
!function($){
	var statusNames	= ['init','submit','pending','completed','error'];
	statusNames[-1] = 'error';
	$('.upload-box').bind({
		dragover: function(e){
			if( !$('.upload-box').hasClass('show'))
				$('.upload-box').addClass('show');	
			return false;
		},
		dragleave: function(e){
			if( e.target.localName == "span")
				if($('.upload-box').hasClass('show')) 
					$('.upload-box').removeClass('show');
			return false;
		},
		drop: function(e){
			e.preventDefault();
			if($('.upload-box').hasClass('show')) 
				$('.upload-box').removeClass('show');
			var files = e.originalEvent.dataTransfer.files;
			displayFiles( files );
			return false;
		}
	});
	$('.upload-box').find('input:file').bind({
			change: function(){
				displayFiles(this.files);
			}		
	});
	function displayFiles(files){
		$('#upload_progress_box').show();		
		$.each( files, function(i, file){
			var $file_item	= $('#upload_progress_box').find('#__prototype').clone();
			$file_item.attr('id','').show();
			$file_item.find('.progress-bar').progressbar({ color: 'bg-darkGreen'});
			$file_item.find('#name')[0].childNodes[1].data = " "+file.name+" ( "+convertSize(file.size)+" )";
			$file_item.appendTo($('#upload_progress_box > .u-panel-content'));
			uploadFile( $file_item, file, window.location.toString());
		});
	}
	function uploadFile( $item, file, url ){
		var formData	= new FormData();
		formData.append('file', file);
		$.ajax({
			url: url,
			data: formData,			
			type: 'PUT',
			xhr: function () {  // custom xhr
                var myXhr = $.ajaxSettings.xhr();
                if (myXhr.upload) { // check if upload property exists
                    myXhr.upload.addEventListener('progress', function (evt) {
                        if (evt.lengthComputable) {
                            var percentComplete = Math.round((evt.loaded * 100) / evt.total);
                            console.log($item.find('.progress-bar'));
                            $item.find('.progress-bar').progressbar('value',percentComplete);
                            $item.find('.progress > span').text(percentComplete + "%");
                        } 
                    }, false); // for handling the progress of the upload
                }
                return myXhr;
            },
			success: function(res){
				$item.find('#install_tlbar').show();
				$item.find('.progress').hide();
				$item.find('#name > i').removeClass('icon-arrow-up-3').addClass('icon-checkmark').addClass('fg-green');
				if(res.update_session_id)
					$item.find('#install_btn').on('click', function(e){
						installUpdate( res.update_session_id );
					});					
			},
			error: function(e){
				$item.find('.progress').hide();
				$item.find('#name > i').removeClass('icon-arrow-up-3').addClass('icon-blocked').addClass('fg-red');
			},
            cache: false,
			contentType: false,
			processData: false
		});
		
	}
	
	function installUpdate( update_session_id ){
		$.ajax({
			url:	window.location.toString().replace(/#.*/g, ''),
			data:	{ update_session_id: update_session_id },
			type:	'POST',
			success:function( data ){
				console.log( data );
				if(data.status)
					getStatus( data.link, function(res){
						return setStatus( JSON.parse(res) );
					} );
			},
			error:	function( data ){
				console.log( "error: "+ data);
			}
		});
	}
	function getStatus( link, cb ){
		$.get(link, function(res){
			if( !cb(res) )
				setTimeout( function(){ getStatus(link, cb); }, 500);
		});
	};
	function setStatus( commands ){
		var $box	= $('#updating_progress_box');
		var $proto	= $('#updating_progress_box > #prototype__update_info');
		var result	= false;
		for(var _c in commands){
			var c = commands[_c];
			$box.show();
			c.forEach( function( c_status ){
				var $agent	= $box.find('div[agent_id="'+c_status.agent_id+'"]');
				if( $agent.length <= 0 ){
					$agent = $proto.clone();
					$agent.show();
					$agent.appendTo($box);
					$agent.attr('agent_id',c_status.agent_id);
					$agent.attr('id','');
					$agent.find('h2').text(c_status.agent_id);
					$.get('/agents?tag='+c_status.agent_id, function( res ){
						if(res.data.length > 0)
							$agent.find('h2').text(res.data[0].name);
					});										
				}
				$agent.find('p').text('Status: '+statusNames[c_status.status] );
				if( c_status.status == 3 )
					result = true;
				if( c_status.status == -1 ){
					$agent.find('#message').text(c_status.message);
					result = true;					
				}					
			});			
		}		
		return result;
	}	
	function convertSize( size ){
		var suffix = ['B','KB','MB','GB','TB'];
		var i = 0;
		while( size > 1024 ){
			size /= 1024;
			i++;
		}
		return size.toFixed(2) + suffix[i];
	}
}(window.jQuery);
