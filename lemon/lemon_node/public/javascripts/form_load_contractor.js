!function(){
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

	$.fn.toggle_panel = function(options){
		return this.each(function(){
			var $this = $(this)
			if(!options){
				var button_template = "<button class='right-box-button' data-button='toggle-panel'><i class='iconi-arrow-up-6'></i></button>"
				var template = "<div class='button-set right-box'></div>"
				if($this.find('.panel-header').find('.button-set').length > 0)
					$this.find('.panel-header').find('.button-set').append($(button_template))
				else
					$this.find('.panel-header').append($(template).append($(button_template)))
				return
			}
			var btn	= options.button
			var hidden = $this.attr('data-hidden')
			if(!hidden){
				$this.find('.panel-content').slideUp(300)
				$this.attr('data-hidden',true)
				btn.find('i').removeClass('iconi-arrow-up-6').addClass('iconi-arrow-down-6')
			}
			else{
				$this.find('.panel-content').slideDown(300)
				$this.removeAttr('data-hidden')
				btn.find('i').removeClass('iconi-arrow-down-6').addClass('iconi-arrow-up-6')
			}
		})
		
	}
	$(document).on('click', '[data-button="toggle-panel"]',function(e){
		e.preventDefault()
		var $this = $(this)
		var options = {}
		options.button	= $this
		$panel = $(this).parents('[data-action="toggle-panel"]')
		$panel.toggle_panel(options)
		
		
	})
	$(document).ready(function(){
		$('[data-action="toggle-panel"]').toggle_panel()
	})
	
}(window.jQuery)