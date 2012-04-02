/* -----------------------------------------------------------------------------
 * Timer and bar on submission page
 * -------------------------------------------------------------------------- */
(function($){
    var time, bar, timer, 
        max_time = $("#timer").attr('data-time-dur')
        now = Date.now(),
        state = 'start';

    var strtime = function(t) {
        var s = t % 60;
        return Math.floor(t / 60) + ":" + (s < 10 ? "0" : "") + s;
    }; 

    // Update bar and time
    timer = window.setInterval(function(){
        var passed = Math.round((Date.now() - now) / 1000),
            perc   = passed/max_time;

        time.text(strtime(max_time - passed));
        bar.width(((1 - perc) * 100) + "%");

        if (state == 'start' && perc > 0.75) {
            state = 'warn';
            bar.parent().removeClass('progress-info')
               .addClass('progress-danger');
        }

        if (passed >= max_time) {
            window.clearInterval(timer);
            time.css('font-color', 'red');
        }
    }, 1000);

    // Build bar and text since those without javascript will have no benefit
    // seeing it
    $("#timer")
        .append(time = 
            $("<div>")
                .text(strtime(max_time))
                .css({
                    'margin-right': 8,
                    'font-weight': 'bold',
                    'float': 'left',
                })
        ).append(
            $("<div>")
                .addClass("progress progress-info")
                .width(500)
                .css('float', 'left')
                .append(bar =
                    $("<div>")
                        .addClass("bar")
                        .width('100%')
                )
        ).append(
            $("<div>")
                .css('clear', 'left')
        );
})(jQuery);
