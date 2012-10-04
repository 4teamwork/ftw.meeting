// This script is placed here, because AT cannot use ++resources++

jq(function(){
    var $start = jq('div#archetypes-fieldname-start_date');
    var $end = jq('div#archetypes-fieldname-end_date');
    
    $start.bind('calendar_after_change', function(e){
        // Get date infos from start_date field
        var year = jq('[id*=year]', $start).attr('value');
        var month = jq('[id*=month]', $start).attr('value');
        var day = jq('[id*=day]', $start).attr('value');
        
        // Update them on end_date field, only if end date is empty
        var end_year = jq('[id*=year]', $end);
        var end_month = jq('[id*=month]', $end);
        var end_day = jq('[id*=day]', $end);
        if (end_year.attr('value') === '0000' && end_month.attr('value') === '00' && end_day.attr('value') === '00'){
            jq('[id*=year]', $end).attr('value', year);
            jq('[id*=month]', $end).attr('value', month);
            jq('[id*=day]', $end).attr('value', day);
        }
        
        
    });
    
});
