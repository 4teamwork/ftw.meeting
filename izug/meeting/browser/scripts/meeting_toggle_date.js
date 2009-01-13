jq(function(){jq('input#no_date').bind('click', function(e){
    
    var targets = jq('select[@name^=start_date_], select[@name^=end_date_]');
    for each (var target in targets) {
        target.disabled == true ? target.disabled=false : target.disabled=true;
    }
    });
    var control = jq('input#no_date')[0];
    var targets = jq('select[@name^=start_date_], select[@name^=end_date_]');
        if (control && control.checked) {
            for each (var target in targets) {
                target.disabled = true ;
            }     
        }else{
            for each (var target in targets) {
                target.disabled = false;            
            }
        }
    
    })
