(function($){
    $.fn.PageControl = function( options ){
        var defaults = {
        };

        var $this = $(this)
            , $ul = $this.children("div").children("ul")
            , $selectors = $ul.find("li div a")
            , $selector_ = $ul.find(".active div")
			, $selector	 = $selector_.children("a")
            , $frames = $this.find(".frames .frame")
            ;

		var initSelectors = function(selectors){
            $.each(selectors, function(i, s){
                if ($(s).parent("li").hasClass("active")) {
                    var target = $(s).attr("href");
					$(target).show();
                }
            })

            selectors.on('click', function(e){
                e.preventDefault();
                var $a = $(this);
                if (!$a.parent('li').hasClass('active')) {
                    $frames.hide();
                    $ul.find("li").removeClass("active");
                    var target = $($a.attr("href"));
                    target.show();
                    $a.parent("div").parent("li").addClass("active");
                }                
            });            
        }

		
		
        return this.each(function(){
            if ( options ) {
                $.extend(defaults, options)
            }
            initSelectors($selectors);			
        });
    }

    $(function () {
        $('[data-role="sidebar-control"]').each(function () {
            $(this).PageControl();
        })
        $(window).resize(function(){
            if ($(window).width() >= 768) {
                $(".page-control ul").css({
                    display: "block"
                    ,overflow: "visible"
                })
            }
            if ($(window).width() < 768 && $(".page-control ul").css("display") == "block") {
                $(".page-control ul").hide();
            }
        })
    })
})(window.jQuery);