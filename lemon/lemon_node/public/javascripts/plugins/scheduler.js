!function($){
	// constances
	dateFormat.masks.standard	= "yyyy-mm-dd HH:MM:ss"
	var main_container
	function getData(selector_container){
		main_container	= selector_container
		var rel_url		= '/tasks'
		var url			= window.location.toString().match(/^(.+\/inventory\/entities\/[-\w]+)/)[1] + rel_url
		var $container	= $(selector_container)
		var $ul			= $container.find('ul.listview')
		var $proto		= $ul.find('#__prototype')
		//$ul.find('li[id^="task_"]').remove()
		$.get( url, function(res){
			var tasks	= res.list
			var set		= combineSets(JSON.parse(localStorage['tasks'] || '[]'),tasks)
			localStorage.setItem('tasks',JSON.stringify(tasks))
			for(var _i in set._old)	{
				var task	= set._old[_i]
				$ul.find("#task_"+task.__id).remove()
			}
			for(var _i in set.both){
				var task	= set.both[_i]
				var item	= $ul.find("#task_"+task.__id)
				if(item.length < 1)
					set._new.push(task)					
				updateTaskInfo(task, item)
			}
			for(var _i in set._new){
				var task	= set._new[_i]
				var item	= $proto.clone()
				item.attr('id','task_' + task.__id)
				updateTaskInfo(task, item)
				item.appendTo($ul)
				item.show()
				item.attr('data-toggle','popover')
				item.attr('data-target','#info_window')				
			}
			function updateTaskInfo(task, item){
				item.find('.data > h4').text(task.content.name)
				item.find('.data > p').text(task.content.func + " " + task.content.kwargs.contractor || "")
				if(task.__enabled)
					item.find('.status').addClass('iconi-clock-5').addClass('fg-color-green')			
				item.on('show.popover', function(e){
					var $this	= $(this)
					$target	= $($this.attr('data-target'))
					$target.find('#title').text(task.content.name || "")
					$target.find('#name').text(task.content.name || "")
					$target.find('#rev').text(task.__revision || 0)
					$target.find('#tags').text(task.__tags || "")
					$target.find('#id').text(task.content.id || "")
					$target.find('#func').text(task.content.func || "")
					$target.find('#args').text(JSON.stringify(task.content.kwargs) || "")
					$target.find('#description').text(task.content.description || "")
					$target.find('#start').text(task.content.start_time || 0)
					$target.find('#interval').text(task.content.interval || 0)
					$target.find('#btn_disable').show()
					$target.find('#btn_enable').show()
					if(task.__enabled)
						$target.find('#btn_enable').hide()					
					else
						$target.find('#btn_disable').hide()
					
						
					$target.find('#btn_enable').on('click', function(e){	_toggleTask($target.find('#name').text(), true)		})
					$target.find('#btn_disable').on('click', function(e){	_toggleTask($target.find('#name').text(), false)	})
					$target.find('#btn_delete').on('click', function(e){	_deleteTask($target.find('#name').text())		})				
				})
				
			}
		})
	}
	function _toggleTask(taskName, enable){
		var rel_url		= '/tasks'
		var url			= window.location.toString().match(/^(.+\/inventory\/entities\/[-\w]+)/)[1] + rel_url
		var cmd			= {}
		if(enable)
			cmd.enable	= true
		else
			cmd.disable	= true
		cmd.name		= taskName
		$.post(url , cmd , function(res){
			if(res.status="ok")
				refresh()
		})
		
	}
	function _deleteTask(taskName){
		var rel_url		= '/tasks'
		var url			= window.location.toString().match(/^(.+\/inventory\/entities\/[-\w]+)/)[1] + rel_url
		var cmd			= {}
		cmd.name		= taskName
		cmd.uninstall	= true
		$.post(url , cmd , function(res){
			if(res.status == "ok") {
				refresh()
			}
		})
	}
	function refresh(){
		getData(main_container)		
	}
	
	function combineSets(oldSet, newSet){
		var set	= {'both': [], '_new': [], '_old': []} // разделяет два множества на три - пересечение, элементы только нового множества, элементы только старого множества
		for(var i in oldSet){
			var current	= oldSet[i]
			var flFound	= false
			for(var j in newSet)
				if(current.__id == newSet[j].__id){
					set.both.push(current)			
					flFound	= true
				}					
			if(!flFound)
				set._old.push(current)
		}
		for(var i in newSet){
			var current = newSet[i]
			var flFound	= false
			for(var j in oldSet)
				if(current.__id == oldSet[j].__id)
					flFound	= true
			if(!flFound)
				set._new.push(current)	
		}		
		return set
	}
	function installPanel(container){
		var formTemplate	= "	<div id='task_add' class='task-add-wrap'>\
									<div class='task-add-header'><button class='close'>×</button><h4>Add new task</h4></div> \
									<div class='task-add-content'><form class='form-inline' method='post'> \
										<input type='hidden' name='install' value='true'>\
										<table><tbody><tr>\
										<td><div class='input-control text span3'><input required id='name' name='name' type='text' placeholder='Name'></div></td>  \
										<td><div class='input-control text span2'><input type='text' name='interval' placeholder='Start interval'></div></td>  \
										<td><div class='input-control text span2'><input type='text' name='start' placeholder='Start time'> </div></td></tr> \
										<tr><td><div class='input-control select'><select name='func' value='runContractor'><option value='runContractor'>runContractor</option></select></div></td><td colspan=2><div class='input-control select'><select required id='c_select' name='contractor'></select></div></td><td>\
										<tr><td colspan=3><div class='input-control textarea '><textarea name='description' maxlength='1024' placeholder='Description'></textarea></td></tr></tbody></table>\
									</form></div> \
									<div class='task-add-footer'><div class='button-set place-right'><button id='reset' class='win-command warning'><span class='win-commandicon win-commandring iconi-cancel-2'></span><span class='win-label'>Reset</span></button>\
									<button id='submit' class='win-command success'><span class='win-commandicon win-commandring iconi-checkmark-5'></span><span class='win-label'>Submit</span></button>\
									</div></div>\
								</div>"
		var $panel		= $(container).parent().parent()
		var $button_set	= $panel.find('.panel-header > .button-set')
		$button_set.find('#add_new_task').click(function(e){
			add_new_task($(this))
		})
	
		function add_new_task(causer){
			if($panel.find('#task_add').length > 0)
			{
				$panel.find('#task_add').find('.close').trigger('click')
				return
			}
			var contractors	= JSON.parse(localStorage.getItem('contractors') || "null")
			if(contractors == "null"){
				var url			= window.location.toString().match(/^(.+\/inventory\/entities\/[-\w]+)/)[1] + '/contractors'
				$.get(url, function(res){
					contractors = res.response
					show_form()						
				})
				return
			}
			show_form()
			function show_form(){
				$form_wrap	= $(formTemplate)
				var $select	= $form_wrap.find('#c_select')
				for(var _i in contractors){
					$select.append($("<option></option>").prop('value',contractors[_i].name).text(contractors[_i].name))
				}
				$form_wrap.hide()
				$form_wrap.prependTo($panel.find('.panel-content'))
				var height	= $panel.find('.panel-content').outerHeight()
				$form_wrap.slideDown(200)
				$form_wrap.find('.close').click(function(e){	$form_wrap.slideUp(200, function(){	$form_wrap.remove()	})		})
				$form_wrap.find('#reset').click(function(e){	reset($form_wrap.find('form'))		})
				$form_wrap.find('#submit').click(function(e){	submit($form_wrap)		})
			}
			function submit($form_wrap){				
				var url			= window.location.toString().match(/^(.+\/inventory\/entities\/[-\w]+)/)[1] + '/tasks'
				var $form		= $form_wrap.find('form')
				$form_wrap.find('.task-add-content').prepend($("<div class='loader-wrap'></div>").append($('<img class="loader" src="/images/preloader-w8-cycle-black.gif">')))
				$.post(url, $form.serialize(), function(res){ 
					if(res.status=='ok'){
						$form_wrap.find('.close').trigger('click')						
						refresh()
					}
					else{
						$form_wrap.find('.loader-wrap').remove()
					}
				})
			}
			function reset($form){
				$form[0].reset()
			}
		}
	}
	$(document).ready(function(){
		getData('#scheduler_container')
		installPanel('#scheduler_container')
		setInterval(refresh, 30000)
	})
	
}(window.jQuery)