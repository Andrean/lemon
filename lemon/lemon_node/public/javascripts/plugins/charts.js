!function($){

	var chart = {}
	chart.CPU		= getCPU_chart
	chart.Memory	= getPhysicalMemory_chart
	
	Highcharts.setOptions({
            global: {
                useUTC: false
            }
        });
	
	function drawChart(containers){
		containers.each(function(){
			chart[$(this).attr('data-contractor')]($(this))
		})
	}
	function getPhysicalMemory_chart(container){
		var startTime	= new Date() - 100*6000
		
		container.highcharts({
			title: {
				text: null
			},
			chart: {
				events: {
					load: function(){
						var series0	= this.series[0];
						var series1	= this.series[1];
						var a= function(start){ 
							var data	= JSON.parse(localStorage.getItem('data')).getSystemInfo
							if(!data)
								return
							var memory		= (JSON.parse(data.value)).memory
							var time		= parseFloat(data.time)*1000
							if(start){
								for(var i=100;i > 0 ; --i)
								{
									series0.addPoint([time - i*5000, 0], false, false)
									series1.addPoint([time - i*5000, 0], false, false)
								}
							}
							series0.addPoint([time, memory.used], true, true)
							series1.addPoint([time, memory.total], true, true)
						}
						a(true)
						setInterval(a, 5000)						
					}
				},				
				height: 300,
				backgroundColor: {
					linearGradient: [330, 0, 330, 500],
					stops: [
						[0, 'rgb(255, 255, 255)'],
						[1, 'rgb(245, 232, 230)']
					]
				},
			},			
			xAxis: {
                type: 'datetime',
                title: {
                    text: null
                }
            },
            yAxis: {
                title: {
                    text: null
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
				},
				min: 0,
				gridLineWidth: 0
            },
            tooltip: {
                shared: true
            },
            legend: {
                enabled: false
            },
            plotOptions: {
                area: {
                    lineWidth: 1,
                    marker: {
                        enabled: false
                    },
                    shadow: false,
                    states: {
                        hover: {
                            lineWidth: 1
                        }
                    },
                    threshold: null
                }
            },
			series: [{
				type: 'area',
				name: 'Allocated Memory',
				data: [],
				color: {
                        linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1},
                        stops: [
                            [0, Highcharts.getOptions().colors[1]],
                            [1, Highcharts.Color(Highcharts.getOptions().colors[1]).setOpacity(0).get('rgba')]
                        ]
                    },
			},{
				type: 'area',
				name: 'Total Memory',
				data: [],
				color: {
                        linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1},
                        stops: [
                            [0, Highcharts.getOptions().colors[0]],
                            [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                        ]
                    },
			}]
		})	
	}
	function getCPU_chart(container){
		container.highcharts({
			title: {
				text: null
			},
			chart: {
				events: {
					load: function(){
						var series	= this.series[0]
						var a = function(start){
							var data	= JSON.parse(localStorage.getItem('data')).getSystemInfo
							if(!data)
								return
							var cpu		= (JSON.parse(data.value)).cpu
							var time	= parseFloat(data.time)*1000
							if(start){
								for(var i=100;i > 0 ; --i)
									series.addPoint([time - i*5000, 0], false, false)								
							}
							if(!isNaN(parseInt(cpu.all)))
								series.addPoint([time, cpu.all], true, true)								
						}
						a(true)
						setInterval(a, 5000)
					}
				},				
				height: 300,
				backgroundColor: {
					linearGradient: [330, 0, 330, 500],
					stops: [
						[0, 'rgb(255, 255, 255)'],
						[1, 'rgb(222, 252, 240)']
					]
				},
			},			
			xAxis: {
                type: 'datetime',
                title: {
                    text: null
                }
            },
            yAxis: {
                title: {
                    text: null
                },
				min: 0,
				max: 100,
				gridLineWidth: 0
            },
            tooltip: {
                shared: true
            },
            legend: {
                enabled: false
            },
            plotOptions: {
                area: {
                    fillColor: {
                        linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1},
                        stops: [
                            [0, Highcharts.getOptions().colors[0]],
                            [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                        ]
                    },
                    lineWidth: 1,
                    marker: {
                        enabled: false
                    },
                    shadow: false,
                    states: {
                        hover: {
                            lineWidth: 1
                        }
                    },
                    threshold: null
                }
            },
			series: [{
				type: 'area',
				data:[]
			}]
		})
	}
	$(document).ready(function(){
		drawChart($('#charts_row').find('[data-contractor]'))
	})
}(window.jQuery)
/*
{"getCPU":{"time":1380218482.903515,"value":"Traceback (most recent call last):\r\n  File \"contractors/60b35285-2edc-4501-b864-1b6253f7fc2c.py\", line 13, in <module>\r\n    response = os.popen(cmd + ' 2>&1','r').read().strip().splitlines()\r\n  File \"contractors/60b35285-2edc-4501-b864-1b6253f7fc2c.py\", line 10, in get_cpu_load\r\n    \r\nIndexError: list index out of range\r\n"},"getPhysicalMemory":{"time":1380218480.643515,"value":"{\"total\": 3215835136, \"value\": 1854763008}\r\n"}} charts.js:146
XHR finished loading: "http://localhost:8080/inventory/entities/c199d833-df45-4543-ac81-ffeed3f8b811/data?contractor=getCPU,getPhysicalMemory". jquery-2.0.3.js:7845
Uncaught SyntaxError: Unexpected token T graphs.js:30
XHR finished loading: "http://localhost:8080/inventory/entities/c199d833-df45-4543-ac81-ffeed3f8b811/data?contractor=getCPU,getPhysicalMemory". jquery-2.0.3.js:7845
{"getCPU":{"time":1380218487.978515,"value":"1\r\n"},"getPhysicalMemory":{"time":1380218480.643515,"value":"{\"total\": 3215835136, \"value\": 1854763008}\r\n"}} charts.js:146
XHR finished loading: "http://localhost:8080/inventory/entities/c199d833-df45-4543-ac81-ffeed3f8b811/data?contractor=getCPU,getPhysicalMemory". jquery-2.0.3.js:7845
XHR finished loading: "http://localhost:80*/