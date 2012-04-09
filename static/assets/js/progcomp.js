/* -----------------------------------------------------------------------------
 * Timer and bar on submission page
 * -------------------------------------------------------------------------- */
(function($){
    var time, bar, timer, 
        elapsed_time = parseInt($("#timer").attr('data-time-elapsed')),
        max_time = parseInt($("#timer").attr('data-time-max')),
        now = Date.now(),
        state = 'start';

    var strtime = function(t) {
        var s = t % 60;
        return Math.floor(t / 60) + ":" + (s < 10 ? "0" : "") + s;
    }; 

    if (!$("#timer").size())
        return;

    // Update bar and time
    var recalc = function(){
        var passed = Math.round((Date.now() - now + elapsed_time*1000) / 1000),
            perc   = passed/max_time;

        time.text(strtime(max_time - passed));
        bar.width(((1 - perc) * 100) + "%");

        if (state == 'start' && perc > 0.5) {
            state = 'mid';
            $("#refresh").removeClass("disabled");
        } else if (state == 'mid' && perc > 0.75) {
            state = 'warn';
            bar.parent().removeClass('progress-info')
               .addClass('progress-danger');
        }

        if (passed >= max_time) {
            window.clearInterval(timer);
            time.css('font-color', 'red');
        }
    };

    timer = window.setInterval(recalc, 1000);

    // Build bar and text since those without javascript will have no benefit
    // seeing it
    $("#timer")
        .text("")
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

    recalc(); // Fire immediately
})(jQuery);

/* -----------------------------------------------------------------------------
 * Fetching diffs with AJAX
 * -------------------------------------------------------------------------- */
(function($){
    $("#submissions").on('click', 'a.failed', function(event){
        event.preventDefault();
        var self = this;
        var link = $(this).attr('href');
        var row = $(this).closest("tr");

        if ($(this).data('fetched')) {
            // Remove and stop
            if ($(this).data('open')) {
                $(this).data('open', false);
                row.next().hide();
            } else {
                $(this).data('open', true);
                row.next().show();
            }
            return;
        }

        // Try loading tiny with js
        $.get(
            link + 'tiny',
            function(response){
                $(self).data('fetched', true);
                $(self).data('open', true);
                row.after(
                    $("<tr>").append(
                        $("<td>")
                            .attr('colspan', row[0].cells.length)
                            .html(response)
                    )
                );
            },
            'html'
        )
        .error(function(){
            // If there was an error trying to fetch it, just redirect the
            // browser instead
            document.location.href = link;
        });
    });
})(jQuery);
