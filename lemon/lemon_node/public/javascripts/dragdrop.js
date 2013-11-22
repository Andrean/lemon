(function($){	
	
	function installDrag(element, maxSize){
		var $element	= $(element)
		var maxFileSize	= maxSize
		$element[0].ondragover = function() {
			$element.addClass('hover');
			return false;
		}
		$element[0].ondragleave = function() {
			$element.removeClass('hover');
			return false;
		}
		$element[0].ondrop = function(e) {
			e.preventDefault()
			$element.removeClass('hover');
			$element.addClass('drop');
        
			var file = event.dataTransfer.files[0];
			if (file.size > maxFileSize) {
				$element.find('div > h3').text('File is too big!');
				$element.addClass('error');
				return false;
			}
			var name	= $element.parents('.modal').attr('contractor_name')			
			var formData	= new FormData();
			formData.append('file',file);
			formData.append('update',true);
			formData.append('name',name);
			var xhr = new XMLHttpRequest();
			xhr.upload.addEventListener('progress', uploadProgress, false);
			xhr.onreadystatechange = stateChange;
			xhr.open('POST', '/inventory/entities/contractors', true);
			xhr.setRequestHeader('X-FILE-NAME', file.name);
			result	= xhr.send(formData);
		}
		
		function uploadProgress(e) {
			var percent = parseInt(e.loaded / e.total * 100);
			$element.find('div > h3').text('Loading: ' + percent + '%');
		}
    
		function stateChange(event) {
			if (event.target.readyState == 4) {
				if (event.target.status == 200) {
					response = jQuery.parseJSON(event.target.response)
					if(response.status == 'ok'){
						var modal = $element.parents('.modal')
						modal.find('#dropbox').hide()
						modal.find('.modal-body').append($('<p></p>').text(response.name))
						modal.find('.modal-body').append($('<p></p>').text(response.size))
						modal.find('.modal-body').append($('<p></p>').text('Rev. '+response.revision))
						modal.find('.modal-header >h3').text('Updated!')
						$element.find('div > h3').text('DROP FILE HERE');
					}
				} else {
					$element.find('div > h3').text('Excepted error!');
					$element.addClass('error');
				}
			}
		}

	}

	$(document).ready(function(){
		installDrag($("#update_modal").find("#dropbox"))
	})
	/*
	var dropZone	= $('#dropZone')
	var maxFileSize	= 1000000
	// Добавляем класс hover при наведении
    dropZone[0].ondragover = function() {
        dropZone.addClass('hover');
        return false;
    };
    
    // Убираем класс hover
    dropZone[0].ondragleave = function() {
        dropZone.removeClass('hover');
        return false;
    };
    
    // Обрабатываем событие Drop
    dropZone[0].ondrop = function(event) {
        event.preventDefault();
        dropZone.removeClass('hover');
        dropZone.addClass('drop');
        
        var file = event.dataTransfer.files[0];
        // Проверяем размер файла
        if (file.size > maxFileSize) {
            dropZone.text('Файл слишком большой!');
            dropZone.addClass('error');
            return false;
        }
        
		
		
        // Создаем запрос
		var formData	= new FormData();
		formData.append('file',file);
        var xhr = new XMLHttpRequest();
        xhr.upload.addEventListener('progress', uploadProgress, false);
        xhr.onreadystatechange = stateChange;
        xhr.open('POST', '/inventory/entities/contractor', true);
        xhr.setRequestHeader('X-FILE-NAME', file.name);
		result	= xhr.send(formData);
    };
	
   // Показываем процент загрузки
    function uploadProgress(event) {
        var percent = parseInt(event.loaded / event.total * 100);
        dropZone.text('Загрузка: ' + percent + '%');
    }
    
    // Пост обрабочик
    function stateChange(event) {
        if (event.target.readyState == 4) {
            if (event.target.status == 200) {
				//console.log(event.target)
				response = jQuery.parseHTML(event.target.response)
				console.log(response)
				if($(response).text() == "none")
				{
					window.alert("Contractor is already exists")
					dropZone.text(">>> Drop file here <<<")	
					return
				}
				$('#fileset > div').append(response)
				setClick()
				dropZone.text(">>> Drop file here <<<")				
            } else {
                dropZone.text('Произошла ошибка!');
                dropZone.addClass('error');
            }
        }
    }*/
})(window.jQuery)