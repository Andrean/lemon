!function($){
	function animateLogo(){
		function animate(opts) {
			var start = new Date; 
			var timer = setInterval(function() {
				var progress = (new Date - start) / opts.duration;
				if (progress > 1) progress = 1;
				opts.step(progress);

				if (progress == 1) clearInterval(timer); // конец :)

			}, opts.delay || 10); // по умолчанию кадр каждые 10мс

		}
		$("#logo > img").on('mouseover', function(){
			var webkit_mask	= $(this).css('-webkit-mask')
			var $this	= $(this)
			var part1 = "-webkit-gradient(radial, 115 26,"
			var radius	= 123
			var width	= 15
			var part2	=", 115 26,"
			var part3	= ", from(rgb(0, 0, 0)), color-stop(0.5, rgba(0, 0, 0, 0.2)), to(rgb(0, 0, 0)))"
			animate({duration: 1000, step: function(progress){
				radius	= progress* 150;
				var prop	= part1 + radius + part2 + (radius+width) + part3
				$this.css('-webkit-mask',prop)
			}})
		})
	}
	$(document).ready(function(){
		animateLogo()
	})
	
}(window.jQuery)