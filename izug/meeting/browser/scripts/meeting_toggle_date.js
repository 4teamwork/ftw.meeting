   
function MeetingTypeSelector(){
        var inpute_meeting_types = jq('input[name=meeting_type]');
        
        var available_schematas = [];
        inpute_meeting_types.each(function(i){
            available_schematas[i] = this.value.split('_');
            })  
        
        jq(available_schematas).each(function(i){
                jq('#fieldsetlegend-'+this).css('display','none');
            })

        inpute_meeting_types.each(function(i){
                jq('#fieldset-'+this).css('display','none');
            }) 
            
            
        //show enabled schematas
        jq('input[name=meeting_type]').each(function(i){
                if (this.checked){
                    var schemata_to_show = this.value.split('_');   
                        jq(schemata_to_show).each(function(i){
                            jq('#fieldset-'+this).toggleClass('hidden');
                        })                    
                    }
            })
        
        inpute_meeting_types.bind('click', function(e){
            
                var schemata_to_show = this.value.split('_');
                
                //hide all schematas - like a reset
                jq(available_schematas).each(function(i){
                        jq('#fieldset-'+this).addClass('hidden');
                    })
                //show the given schematas
                jq(schemata_to_show).each(function(i){
                        jq('#fieldset-'+this).toggleClass('hidden');
                    })
                
            })
    }

jq(MeetingTypeSelector);
