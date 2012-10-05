
function MeetingTypeSelector(){
  var inpute_meeting_types = jq('input[name=meeting_type]');

  var available_schematas = [];
  inpute_meeting_types.each(function(i){
                              available_schematas[i] = this.value;
                            });


  available_schematas = jq.map(available_schematas, function(n){return n;});

  // hide legends
  jq(available_schematas).each(function(i){
                                 jq('#fieldsetlegend-'+this).parents('.formTab').hide();
                               });

  // re-add .lastFormTab class, if we removed the last legend
  jq('.formTab:visible:last').addClass('lastFormTab');

  // hide fieldsets
  inpute_meeting_types.each(function(i){
                              jq('#fieldset-'+this).hide();
                            });

  //show enabled schematas
  inpute_meeting_types.each(function(i){
                              if (this.checked){
                                var schemata_to_show = this.value.split('_');
                                jq(schemata_to_show).each(function(i){
                                                            jq('#fieldset-'+this).show();
                                                          });
                              }
                            });

  inpute_meeting_types.bind('click', function(e){

                              var schemata_to_show = this.value.split('_');

                              //hide all schematas - like a reset
                              jq(available_schematas).each(function(i){
                                                             jq('#fieldset-'+this).hide();
                                                           });

                              //show the given schematas
                              jq(schemata_to_show).each(function(i){
                                                          jq('#fieldset-'+this).show();
                                                        });

                            });

}

jq(MeetingTypeSelector);


function MeetingItemToggler(){
        jq('.MeetingItemHead').click(function(e){
                e.preventDefault();
                var parentItem = jq(this).closest('.MeetingItemWrapper');
                var meetingBody = jq('#'+parentItem.attr('id') + ' .MeetingItemBody');

                if (meetingBody.css('display') != 'none'){
                        jq('#'+parentItem.attr('id') + ' .MeetingItemBody').hide('blind', 100);
                        jq('#'+parentItem.attr('id') + ' .MeetingItemHead .toggleImage').attr('src',portal_url+'/++resource++meeting-styles/arrow_right.png');
                    }
                else {
                        jq('#'+parentItem.attr('id') + ' .MeetingItemBody').show('blind', 100);
                        jq('#'+parentItem.attr('id') + ' .MeetingItemHead .toggleImage').attr('src',portal_url+'/++resource++meeting-styles/arrow_down.png');
                    }


            }).children('.meetingItemActions').click(function(event) {event.stopPropagation();});;
    }
jq(MeetingItemToggler);
