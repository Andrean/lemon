/**
 *  	/configuration/agents.js client script 
 */
!function($){
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
			$('#upload_progress_box').find('#file_item > div > h2')[0].childNodes[1].data = " "+file.name+" ( "+convertSize(file.size)+" )";
			uploadFile( file, window.location.toString());
		});
	}
	function uploadFile( file, url ){
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
                            $('#upload_progress_box').find('.progress-bar').progressbar('value',percentComplete);
                            $('#upload_progress_box').find('.progress > span').text(percentComplete + "%");
                        } 
                    }, false); // for handling the progress of the upload
                }
                return myXhr;
            },
			success: function(res){
				$('#upload_progress_box').find('#install_tlbar').show();
				$('#upload_progress_box').find('.progress').hide();
				$('#upload_progress_box').find('#file_item > div > h2 > i').removeClass('icon-arrow-up-3').addClass('icon-checkmark').addClass('fg-green');
				if(res.update_session_id)
					$('#upload_progress_box').find('#install_btn').on('click', function(e){
						installUpdate( res.update_session_id );
					});					
			},
			error: function(e){
				$('#upload_progress_box').find('.progress').hide();
				$('#upload_progress_box').find('#file_item > div > h2 > i').removeClass('icon-arrow-up-3').addClass('icon-blocked').addClass('fg-red');
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
					checkStatus( data.link, function(res){
						console.log( res );
					} );
			},
			error:	function( data ){
				console.log( "error: "+ data);
			}
		});
	}
	function checkStatus( link, cb ){
		$.get(link, function(res){
			if( !cb(res) )
				setTimeout( function(){ checkStatus(link, cb); }, 500);
		});
	};
	
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
