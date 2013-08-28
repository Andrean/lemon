
$(document).ready(function(){
	function setPhysicalMemoryChart(_dataTotal, _dataAllocated){
		$('#PhysicalMemoryChart').highcharts({
            chart: {
                type: 'areaspline',
				animation: Highcharts.svg,
				marginRight: 10,
                events: {
                    load: function() {    
                        var freeMemorySeries = this.series[1];
						var totalMemorySeries = this.series[0];
						var total;
						setInterval(function() {
								$.get(window.location + "/data?contractor=getAllocatedPhysicalMemory,getTotalPhysicalMemory", function(result){
									console.log(result.data)
									var x = result.data.getAllocatedPhysicalMemory.time*1000;
									var y = parseFloat(result.data.getAllocatedPhysicalMemory.value);
									var total = parseFloat(result.data.getTotalPhysicalMemory.value);
									freeMemorySeries.addPoint([x, y], true, true);
									totalMemorySeries.addPoint([x, total], true, true);
								});
                        }, 30000);
                    }
                }
            },
            title: {
                text: 'Physical Memory'
            },
            xAxis: {
				type: 'datetime',
                tickPixelInterval: 150                
            },
            yAxis: {
                title: {
                    text: 'Physical memory value, Mb'
                },
                labels: {
                    formatter: function() {
						var prefix = ['b','Kb','Mb','Gb','Tb']
						var lastPrefix	= 0;
						var value	= this.value;
						while (value > 1024)
						{
							value /= 1024;
							lastPrefix += 1;							
						}
						if(lastPrefix >= prefix.length){
								value *= (prefix.length - lastPrefix - 1)*1024
								lastPrefix = prefix.length - 1
						}
						
                        return value.toFixed(0)  + ' ' + prefix[lastPrefix];
                    }
                }				
            },
            tooltip: {
                formatter: function() {
                        return '<b>'+ this.series.name +'</b><br/>'+
                        Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) +'<br/>'+
                        Highcharts.numberFormat(this.y, 0) + " b";
                }
            },
            plotOptions: {
                areaspline: {
                    marker: {
                        enabled: false,
                        symbol: 'circle',
                        radius: 2,
                        states: {
                            hover: {
                                enabled: true
                            }
                        }
                    }
                }
            },
            series: [
				{
				type: 'areaspline',
                name: 'Total Physical Memory',
                data: (function(){
					var data = []
                    for (i = 0; i < _dataTotal.length; i++) {
						data.push({
                            x: _dataTotal[i].time*1000,
                            y: _dataTotal[i].value
                        });
                    }
					return data
				})()
            }	,		{
				type: 'areaspline',
                name: 'Allocated Physical Memory',
                data: (function(){
					var data = []
                    for (i = 0; i < _dataAllocated.length; i++) {
						data.push({
                            x: _dataAllocated[i].time*1000,
                            y: _dataAllocated[i].value
                        });
                    }
					return data
				})()
            }]
        });
	}
	function setCPULoadChart(_data){	
		Highcharts.setOptions({
            global: {
                useUTC: false
            }
        });
    
        var chart;
        $('#container').highcharts({
            chart: {
                type: 'spline',
                animation: Highcharts.svg, // don't animate in old IE
                marginRight: 10,
                events: {
                    load: function() {    
                        // set up the updating of the chart each second
                        var series = this.series[0];
                        setInterval(function() {
								$.get(window.location + "/data?contractor=getCPU", function(result){									
									var x = result.data.getCPU.time*1000, // current time
									y = parseInt(result.data.getCPU.value);
									series.addPoint([x, y], true, true);
								})
                        }, 10000);
                    }
                }
            },
            title: {
                text: 'CPU Load Percentage'
            },
            xAxis: {
                type: 'datetime',
                tickPixelInterval: 150
            },
            yAxis: {
                title: {
                    text: 'Load'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }],
				min : 0,
				max : 100,
				minorGridLineWidth: 0,
                gridLineWidth: 1,
                alternateGridColor: null,
				plotBands: [{ //normat load
						from: 0,
						to : 25,
						color: 'rgba(175, 213, 217, 0.2)'
					},{	// loaded
						from: 25,
						to : 50,
						color: 'rgba(147, 211, 217, 0.2)'
					},{ // overload
						from: 50,
						to : 90,
						color: 'rgba(181, 146, 114, 0.2)'
					},{ 
						from: 90,
						to : 100,
						color: 'rgba(159, 98, 43, 0.2)'					
					}]
				
            },
			tooltip: {
                formatter: function() {
                        return '<b>'+ this.series.name +'</b><br/>'+
                        Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) +'<br/>'+
                        Highcharts.numberFormat(this.y, 2);
                }
            },
			plotOptions: {
                spline: {
                    lineWidth: 3,
                    states: {
                        hover: {
                            lineWidth: 5
                        }
                    },
                    marker: {
                        enabled: false
                    }                    
                }
            },
            legend: {
                enabled: false
            },
            exporting: {
                enabled: false
            },
            series: [{
                name: 'CPU load',
                data: (function() {
					var data = []
                    for (i = 0; i < _data.length; i++) {
						data.push({
                            x: _data[i].time*1000,
                            y: _data[i].value
                        });
                    }
                    return data;
                })()
            }]
        });
	}
	function setClick(){
		$("button[id$='_install']").on('click', function(event){
			event.stopPropagation()
			var id_s	= $(this).attr('id')
			var re 		= /\d+/
			var num 	= id_s.match(re)[0]
			var filename	= $('#name'+num+' a').text()
			var name	= filename.match(/\w+/)[0]
			$.post('/inventory/entities/contractor',{'install':true,'name':name}, function(res){
				if(res.status	 == 'installed'){
					$("#btn"+num+"_install").detach()
					$("#not_installed"+num).detach()
					$('#row_header'+num).prepend('<div id="installed'+num+'" class="installed"></div>')
					$('#installed'+num).append('<i class="icon-checkmark"></i>')				
				}
			}, "json")
		})
		$("button[id$='_delete']").on('click', function(event){
			event.stopPropagation()
			var id_s	= $(this).attr('id')
			var re 		= /\d+/
			var num 	= id_s.match(re)[0]
			var filename	= $('#name'+num+' a').text()
			var name	= filename.match(/\w+/)[0]
			console.log('"' + name+'"')
			$.post('/inventory/entities/contractor', {'install': false,'name':name}, function(res){
				if(res.status=="deleted")
					$('#row'+num).detach()		
			})
		})
		// установить обработчик запись, чтобы выезжала форма по клику
		
	}
	function setClicks(){
		$("div[id^='row_header']").on('click', function(event){
			event.stopPropagation()
			var id_s	= $(this).attr('id')
			var num 	= id_s.match(/\d+/)[0]
			if($('#form_scheduler'+num).css('display') == 'none')
				$('#form_scheduler'+num).slideDown(1000)
			else{
				$('#form_scheduler'+num).slideUp(1000)
				console.log("animating")
				}
			parent	= $("#row"+num)
			if(parent.css("height") == "50px")
				parent.animate({height:'360px'},1000)
			else
				parent.animate({height:'50px'},1000)
		})
		$("input[id^='disable_task_wrap']").click(function(e){
			event.stopPropagation()
			var id_s	= $(this).attr('id')
			var num 	= id_s.match(/\d+/)[0]
			var task	= $("#form"+num+"_taskname").val()
			$.post('/inventory/entities/task', {'disable': true, 'task_name': task }, function(res){
				if(res.status =="ok"){
					$("#disable_task_wrap"+num).hide()
					$("#submit"+num).val('setup')
				}
			})
		})
	}
	function submitValidator(){
		$("form[id^='form']").submit(function(e){
			var id_s	= $(this).attr('id')
			var num 	= id_s.match(/\d+/)[0]
			e.stopPropagation()
			var action		= $(this).attr('action')
			var task_name	= $("#form"+num+"_taskname").val()
			var interval	= $("#form"+num+"_interval").val()
			var start_time	= $("#form"+num+"_starttime").val()
			var contractor	= $("#form"+num+"_contractor").val()
			var formData	= {}
			formData['task_name'] =  task_name
			formData['interval'] 	= interval
			formData['start_time']	= start_time
			formData['contractor']	= contractor
			$.post('/inventory/entities/task', formData, function(result){
				if(result.status	== 'ok')
				{
					$("#submit"+num).val('change')
					$("#disable_task_wrap"+num).show()
					setClick()
				}
				if(result.status	== "error")
				{
					window.alert("error")
				}
					
			})
			return false;
		})
	}
	function setChange(){
		$("input[id^='check_onetime']").on('change', function(e){
			var id_s	= $(this).attr('id')
			var num 	= id_s.match(/\d+/)[0]
			if($(this).is(':checked'))
			{
				$('#form_row_starttime'+num+' > label').removeClass('disabled')
				$('#form_row_starttime'+num+' > div > input[type="datetime-local"]').removeAttr('disabled')
				$('#form_row_interval'+num+' > label').addClass('disabled')
				$('#form_row_interval'+num+' > div > input[type="time"]').attr('disabled', true)
			}
			else{
				$('#form_row_starttime'+num+' > label').addClass('disabled')
				$('#form_row_starttime'+num+' > div > input[type="datetime-local"]').attr('disabled',true)
				$('#form_row_interval'+num+' > div > input[type="time"]').removeAttr('disabled')
				$('#form_row_interval'+num+' > label').removeClass('disabled')
			}
		})
	}
	var setTasksClick	= function()	{
		$("button[id^='btn_delete_task']").on('click', function(event){
			event.stopPropagation()
			var id_s	= $(this).attr('id')
			var id		= id_s.match(/btn_delete_task([\w\-]+)/)[1]
			$.get(window.location+"/tasks?delete="+id, function(result){
				if(result.status	== 'error')
					alert("Error while removing")
				else{
					$("#removing_bar"+id).show()
					$("#btn_delete_task"+id).hide()
				}
			})
			console.log(id)
			
		})
	}
	var renew	= function(){
		$.get(window.location+"/tasks?show_agent=1", function(data){
			response	= jQuery.parseHTML(data)
			console.log(response)
			$("#taskset > ul").detach()
			$("#taskset").append(response)			
		})
		$.get(window.location+"/tasks", function(data){
			_response	= jQuery.parseHTML(data)
			$("#mtaskset > ul").detach()
			$("#mtaskset").append(_response)
			setTasksClick()
		})
	}
	function setCharts(){
		var x = (new Date()).getTime()/1000 - 120
		var _data	= []
		var _dataTotal = []
		var _dataAllocated = []
		var time, value, total= -1;
		$.get(window.location + "/data?contractor=getCPU,getAllocatedPhysicalMemory,getTotalPhysicalMemory&from="+x, function(results){			
			for(var v in results.data){
				for(var k in results.data[v].data){
					if(results.data[v].data[k].name == "getCPU"){
							time	= results.data[v].data[k].start_time
							value	= parseFloat(results.data[v].data[k].result)
							_data.push({'time': time, 'value': value})
					}
					if(results.data[v].data[k].name == "getAllocatedPhysicalMemory"){
							time	= results.data[v].data[k].start_time
							value	= parseFloat(results.data[v].data[k].result)
							_dataAllocated.push({'time': time, 'value': value})
					}
					if(results.data[v].data[k].name == "getTotalPhysicalMemory"){
							time	= results.data[v].data[k].start_time
							if(total = -1)
								total	= parseFloat(results.data[v].data[k].result)
							_dataTotal.push({'time': time, 'value': total})
					}
				}
			}
			setCPULoadChart(_data)
			setPhysicalMemoryChart(_dataTotal, _dataAllocated)		
		})		
	}
	
	renew()
	setInterval(renew, 10000)
	setCharts()
	$('.sidebar').css('height', $(document).height() - $("#page1").height() - 70)
	$(window).resize(function(e){
		$('.sidebar').css('height', $(document).height() - $("#page1").height() - 70)
	})
	
	$.post('',{'contractor': 'get'}, function(data){
		response = jQuery.parseHTML(data)
		$("#fileset > div").append(response)
		setClick()
		setChange()
		setClicks()
		submitValidator()
	})
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
    }

	
	
});