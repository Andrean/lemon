!function($){
	$.fn.toggle_element	= function(options){
		return this.each(function(){
			var $this = $(this);
			var $target	= $($this.attr('data-target'));
			var $aria_state	= $this.attr('aria-hidden');
			var $alt_text	= $this.attr('alt-text');
			if($aria_state == 'true'){
				$target.show();
				$this.attr('aria-hidden','false');
				$this.attr('alt-text', $this.text());
				$this.removeClass('default').addClass('info').text($alt_text);
			}
			else{
				$target.hide();
				$this.attr('aria-hidden','true');
				$this.attr('alt-text', $this.text());
				$this.removeClass('info').addClass('default').text($alt_text);
			}	
		});
	};
	
	$.fn.serializeObject = function(){

        var self = this,
            json = {},
            push_counters = {},
            patterns = {
                "validate": /^[a-zA-Z][a-zA-Z0-9_]*(?:\[(?:\d*|[a-zA-Z0-9_]+)\])*$/,
                "key":      /[a-zA-Z0-9_]+|(?=\[\])/g,
                "push":     /^$/,
                "fixed":    /^\d+$/,
                "named":    /^[a-zA-Z0-9_]+$/
            };


        this.build = function(base, key, value){
            base[key] = value;
            return base;
        };

        this.push_counter = function(key){
            if(push_counters[key] === undefined){
                push_counters[key] = 0;
            }
            return push_counters[key]++;
        };

        $.each($(this).serializeArray(), function(){

            // skip invalid keys
            if(!patterns.validate.test(this.name)){
                return;
            }

            var k,
                keys = this.name.match(patterns.key),
                merge = this.value,
                reverse_key = this.name;

            while((k = keys.pop()) !== undefined){

                // adjust reverse_key
                reverse_key = reverse_key.replace(new RegExp("\\[" + k + "\\]$"), '');

                // push
                if(k.match(patterns.push)){
                    merge = self.build([], self.push_counter(reverse_key), merge);
                }

                // fixed
                else if(k.match(patterns.fixed)){
                    merge = self.build([], k, merge);
                }

                // named
                else if(k.match(patterns.named)){
                    merge = self.build({},k, merge);
                }
            }

            json = $.extend(true, json, merge);
        });

        return json;
    };
	
	$(document).on('click','[data-role="toggle"]', function(e){
		e.preventDefault();
		var $this	= $(this);
		$this.toggle_element();
	});
	
	$('a[data-role="toggle-click"]').click(function(e){
		var $this	= $(this);
		var $target	= $($this.attr('data-target'));
		$target.toggle();
	});
	$(document).ready(function(){
		$('[is-hidden="true"]').hide();
		$('[is-hidden="false"]').show();		
	});
	
}(window.jQuery);