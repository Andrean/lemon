!function($){
	
	$.fn.popover	= function(options){
		return this.each(function(){
			var $this = $(this)
			var related	= options.related
			var offset	= related.offset()
			var container	= options.container
			
			$this.appendTo(container)
			$this.css('top', offset.top)
			$this.css('left', offset.left + related.outerWidth() + 14)
			$this.attr('data-popover','true')
			$this.show()			
			$(document).one('click.popover.close',function(e){
				e.stopPropagation()				
				$this.hide()
				$this.removeAttr('data-popover')
				related.removeClass('c-selected')
			})
			//var e	= $.Event('shown.popover')
			//related.trigger(e)
		})
	}	
	$(document).on('click','[data-toggle="popover"]', function(e){
		e.preventDefault()
		var options	= {}
		var $this = $(this)
		var $target	= $($this.attr('data-target'))
		options.related		= $this
		options.container	= 'body'
		if($this.hasClass('c-selected'))
			return
		if($target.attr('data-popover') == 'true')
			return
		var e	= $.Event('show.popover')
		$this.trigger(e)
		$this.addClass('c-selected')
		$target.popover(options)		
	})	
	
}(window.jQuery)