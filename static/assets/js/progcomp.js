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
    var toggle_row = function(diff_row, attempt_row) {
        if (diff_row.parent().length == 0) {
            // Append
            attempt_row.after(diff_row);
            attempt_row.find("td:first-child").attr('rowspan', '2');
        } else {
            // Remove
            diff_row.remove();
            attempt_row.find("td:first-child").attr('rowspan', '1');
        }
        return;
    };

    $("#submissions").on('click', 'a.failed', function(event){
        event.preventDefault();
        var self = this;
        var link = $(this).attr('href');
        var row = $(this).closest("tr");
        var diff = $(this).data('diff');

        // If we already loaded once, just toggle
        if (diff)
            return toggle_row(diff, row);

        // Try loading tiny with js
        $.get(
            link + 'tiny/',
            function(response){
                var diff_row = $("<tr>").append(
                                    $("<td>")
                                        .attr('colspan', row[0].cells.length - 1)
                                        .html(response));
                $(self).data('diff', diff_row);
                toggle_row(diff_row, row);
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

/* -----------------------------------------------------------------------------
 * Sort function for tables
 * -------------------------------------------------------------------------- */
(function($){
    var sort = {col: null, dir: 0};

    // Returns true if a should be placed higher than b
    var cmp = function(a, b) {
        return (a.value == b.value) || (a.value > b.value) ^ sort.dir;
    };

    // Generic; mutates array
    var mergesort = function(arr, i, j) {
        // Initial call
        if (i == undefined || j == undefined)
            return mergesort(arr, 0, arr.length);

        // Base case
        if (i >= j - 1)
            return;

        // Break in half
        var part = Math.ceil((i+j)/2);
        mergesort(arr, i, part);
        mergesort(arr, part, j);

        // Merge
        var store = [];
        for (var pi=i, pj=part; pi < part || pj < j;)
            if (pi < part && (pj >= j || cmp(arr[pi], arr[pj])))
                store.push(arr[pi++]);
            else if (pj < j)
                store.push(arr[pj++]);
        for (var k = i; k < j; k++)
            arr[k] = store[k - i];
    };

    $("table.sortable").each(function(){
        var def = $(this).find("th[data-sort]");
        var tbl = this;
        if (def.length > 0) {
            sort.col = def[0];
            sort.dir = def.attr('data-sort') == "desc" ? 0 : 1;
        }

        $(this).find('th').each(function(){
            $(this)
                .css('cursor', 'pointer')
                .append($("<i>").addClass("icon-chevron-down").css('visibility', 'hidden'));
        });
        $(this).on('click', 'th', function(){
            if (this != sort.col) {
                $(tbl).find("th > i").css('visibility', 'hidden');
                sort.col = this;
                sort.dir = 0;
            } else {
                sort.dir = 1 - sort.dir;
            }
            $(this).find("i").removeClass().addClass("icon-chevron-" + (sort.dir > 0 ? "up" : "down")).css('visibility', 'visible');
            var col = this.cellIndex;

            // sort items via stable sort
            var rows = $(tbl).find("tbody>tr").map(function(_, tr){
                var cell = $(tr.cells[col]).text();
                return { row: tr, value: parseFloat(cell) || cell };
            });
            mergesort(rows);
            for (var i = 0; i < rows.length; i++)
                $(tbl).find("tbody").append(rows[i].row);
        });
    });
})(jQuery);

/* -----------------------------------------------------------------------------
 * Automatic update for submissions
 * -------------------------------------------------------------------------- */
var opts = { // Customize at http://fgnass.github.com/spin.js/
    lines: 13, // The number of lines to draw
    length: 0, // The length of each line
    width: 2, // The line thickness
    radius: 5, // The radius of the inner circle
    rotate: 0, // The rotation offset
    color: '#000', // #rgb or #rrggbb
    speed: 1, // Rounds per second
    trail: 60, // Afterglow percentage
    shadow: false, // Whether to render a shadow
    hwaccel: false, // Whether to use hardware acceleration
    className: 'spinner', // The CSS class to assign to the spinner
    zIndex: 2e9, // The z-index (defaults to 2000000000)
    top: 'auto', // Top position relative to parent in px
    left: 'auto' // Left position relative to parent in px
};
(function($){
    var spinner, graders, last_query;

    graders = $("td[data-loading]");
    if (!graders.size())
        return;

    $.fn.spin = function(opts) {
        this.each(function() {
            var $this = $(this),
                data  = $this.data();

            if (data.spinner) {
                data.spinner.stop();
                delete data.spinner;
            }
            if (opts !== false) {
                data.spinner = new Spinner($.extend({color: $this.css('color')}, opts)).spin(this);
            }
        });
        return this;
    };

    // Start all spinners
    graders.spin(opts);

    // Query every second until we are out
    var query = function(){
        // Stop when we resolve every grader
        if (!graders.size())
            return;

        last_query = Date.now();
        $.get(
            "/submit/json",
            { submissions: graders.map(function(){ return $(this).attr('data-loading'); }).get().join(',') },
            function success(data){
                for (var i in data) {
                    var attempt;
                    attempt = graders.filter("[data-loading="+i+"]");
                    if (attempt.length == 1) {
                        // Found a newly graded item, remove it from the jQuery list
                        graders = graders.not(attempt);
                        attempt.spin(false);
                        if (data[i].indexOf("diff") == -1) {
                            // No diff means we display status as plain text
                            attempt.text(data[i]);
                        } else {
                            // Failed and returned diff
                            attempt.html("<a href='" + data[i] + "'>Failed</a>");
                        }
                    }
                }

                // Follow up success with another timer
                // Stop if the response took more than 2s; we don't want to put
                // additional burden on the server
                if (Date.now() - last_query < 2000)
                    window.setTimeout(query, 3000);
                else
                    graders.spin(false);
            },
            'json'
        )
        .error(function(a,b,c){
            // Stop all spinners to let user know that further attempts will be halted
            graders.spin(false);
        });
    };

    // Set initial timer
    window.setTimeout(query, 1000);
})(jQuery);
