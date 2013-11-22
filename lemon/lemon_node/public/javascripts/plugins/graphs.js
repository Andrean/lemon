!function($){
	var inputs	= {}
	var keys = []
	var input_disks	= []
	function getList(circleStatRow){
		var $row	= $(circleStatRow);
		$row.find('.circleStatsItemBox').each(function(){
			var $this	= $(this)
			inputs[$this.attr('data-contractor')] = $this.find('#circle')
			keys.push($this.attr('data-contractor'))
		})
	}
	function getData(_keys){
		var system_info	= JSON.parse(localStorage.getItem('data')).getSystemInfo
		var time	= system_info.time
		var data	= JSON.parse(system_info.value)
		for(var i in _keys){
			refreshCircleGraph(_keys[i],data[_keys[i]])
		}		
	}
	function diskRefresh(data){
		if(input_disks.length < 1)
		{	
			var proto	= inputs['disk']
			for(var i in data){
				var bbox	= proto.parents('.circleStatsItemBox').parent().clone()
				bbox.appendTo(proto.parents('.circleStatsItemBox').parent().parent())
				bbox.show()
				var disk	= bbox.find('#circle')
				disk.knob({
					min: 0,
					max: 100,
					width: 120,
					inputColor: "#fff",
					fgColor: "#fff",
					bgColor: "rgba(255,255,255,0.4)",
					readOnly: true
				})
				disk.attr('data-partition', data[i].partition)
				input_disks.push(disk)
			}
		}
		for(var i in data){
			var partition	= data[i]
			var disk = {}
			for(var j in input_disks){
				if(input_disks[i].attr('data-partition') == partition.partition)
					disk = input_disks[i]
			}
			var current	= parseInt(disk.val())
			var diff	= partition.usage.percent - current
			var box	= disk.parents('.circleStatsItemBox')
			box.find('.header').text('Disk ' + partition.partition + ' space usage')
			var footer	= box.find('.footer')
			var count	= footer.find('.count').find('.number')
			var countUnit	= footer.find('.count').find('.unit')
			var total	= footer.find('.value').find('.number')
			var totalUnit	= footer.find('.value').find('.unit')
			disk
				.val((current + diff).toFixed(0))
				.trigger('change')
			count.text(formatSize(partition.usage.used))
			total.text(formatSize(partition.usage.total))
			
		}
	}
	function refreshCircleGraph(contractor, data){
		var input	= inputs[contractor]
		var current	= parseInt(input.val())
		var res		= data
		if(contractor == 'cpu')
			res	= {'used': res.all, 'total': 100, 'percent': res.all }			
		if(contractor == 'disk'){
			diskRefresh(data)
			return 
		}
		var diff	= res.percent - current
		var footer	= input.parents('.circleStatsItemBox').find('.footer')
		var count	= footer.find('.count').find('.number')
		var countUnit	= footer.find('.count').find('.unit')
		var total	= footer.find('.value').find('.number')
		var totalUnit	= footer.find('.value').find('.unit')		
		animate({duration: 100, step: function(progress){
			input
				.val((current + diff*progress).toFixed(0))
				.trigger('change')
			count.text(formatSize((current + diff*progress)*res.total / 100))
			total.text(formatSize(res.total))
		}})
		
	}
	function formatSize(num){
		if(num > 100)
		{
			num /= 1024*1024*1024
			return num.toFixed(2)
		}
		return num.toFixed(0)
		
	}
	function animate(opts) {
			var start = new Date; 
			var timer = setInterval(function() {
				var progress = (new Date - start) / opts.duration;
				if (progress > 1) progress = 1;
				opts.step(progress);

				if (progress == 1) clearInterval(timer); // конец :)

			}, opts.delay || 10); // по умолчанию кадр каждые 10мс

	}
	$(document).ready(function(){
		getList('.circleStats')
		getData(keys)
		for(var i in inputs){
				inputs[i].knob({
				min: 0,
				max: 100,
				width: 120,
				inputColor: "#fff",
				fgColor: "#fff",
				bgColor: "rgba(255,255,255,0.4)",
				readOnly: true
			})
		}
		setInterval(function(){ getData(keys)}, 5000)
	})	
}(window.jQuery)