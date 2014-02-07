/**
 * 		Page Configuration - Plugins
 */
!function($){
	function modern_switch_tab( options, element ){
		var $target	= $(options.target);
		var $container	= $(options.container);
		if($target.is(':hidden')){
			$container.children(':not('+options.target+')').hide('slide',{direction: 'left'}, 300, function(){
				element.attr('data-switched','true');
				$target.show('slide',{direction: 'right'},300);
			});				
		}
	}
	function backward_tab( options, element ){
		var $target	= $(options.target);
		$(options.hide).hide('slide',{direction: 'left'}, 300, function(){
			$target.show('slide',{direction: 'right'},300);
		});		
	}
	$(document).on('click','[data-role="modern-switch-tab"]', function(){
		var $this	= $(this);
		var target	= $this.attr('data-target');
		var container	= $this.attr('data-container');		
		modern_switch_tab({ target: target, container: container }, $this);
		return false;
	});
	$(document).on('click','[data-action="backward-tab"]', function(){
		var $this	= $(this);
		var target	= $this.attr('data-target');
		var to_hide = $this.attr('data-hide');
		backward_tab({ target: target, hide: to_hide }, $this);
		return false;
	});
}(window.jQuery);
