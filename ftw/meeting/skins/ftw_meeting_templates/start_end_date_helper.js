// This script is placed here, because AT cannot use ++resources++

jQuery(function($){
    var $start = $('div#archetypes-fieldname-start_date');
    var $end = $('div#archetypes-fieldname-end_date');

    $start.bind('calendar_after_change', function(e){
        // Get date infos from start_date field
        var year = $('[id*=year]', $start).attr('value');
        var month = $('[id*=month]', $start).attr('value');
        var day = $('[id*=day]', $start).attr('value');

        // Update them on end_date field, only if end date is empty
        var end_year = $('[id*=year]', $end);
        var end_month = $('[id*=month]', $end);
        var end_day = $('[id*=day]', $end);
        if (end_year.attr('value') === '0000' && end_month.attr('value') === '00' && end_day.attr('value') === '00'){
            $('[id*=year]', $end).attr('value', year);
            $('[id*=month]', $end).attr('value', month);
            $('[id*=day]', $end).attr('value', day);
        }


    });

});
