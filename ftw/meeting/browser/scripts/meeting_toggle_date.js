function MeetingTypeSelector(){
  var inpute_meeting_types = $('input[name=meeting_type]');

  var available_schematas = [];
  inpute_meeting_types.each(function(i){
                              available_schematas[i] = this.value;
                            });


  available_schematas = $.map(available_schematas, function(n){return n;});

  // hide legends
  $(available_schematas).each(function(i){
                                 $('#fieldsetlegend-'+this).parents('.formTab').hide();
                               });

  // re-add .lastFormTab class, if we removed the last legend
  $('.formTab:visible:last').addClass('lastFormTab');

  // hide fieldsets
  inpute_meeting_types.each(function(i){
                              $('#fieldset-'+this).hide();
                            });

  //show enabled schematas
  inpute_meeting_types.each(function(i){
                              if (this.checked){
                                var schemata_to_show = this.value.split('_');
                                $(schemata_to_show).each(function(i){
                                                            $('#fieldset-'+this).show();
                                                          });
                              }
                            });

  inpute_meeting_types.bind('click', function(e){

                              var schemata_to_show = this.value.split('_');

                              //hide all schematas - like a reset
                              $(available_schematas).each(function(i){
                                                             $('#fieldset-'+this).hide();
                                                           });

                              //show the given schematas
                              $(schemata_to_show).each(function(i){
                                                          $('#fieldset-'+this).show();
                                                        });

                            });

}

$(MeetingTypeSelector);


function MeetingItemToggler(){
        $('.MeetingItemHead').click(function(e){
                e.preventDefault();
                var parentItem = $(this).closest('.MeetingItemWrapper');
                var meetingBody = $('#'+parentItem.attr('id') + ' .MeetingItemBody');

                if (meetingBody.css('display') != 'none'){
                        $('#'+parentItem.attr('id') + ' .MeetingItemBody').hide(100);
                        $('#'+parentItem.attr('id') + ' .MeetingItemHead .toggleImage').attr('src',portal_url+'/++resource++meeting-styles/arrow_right.png');
                    }
                else {
                        $('#'+parentItem.attr('id') + ' .MeetingItemBody').show(100);
                        $('#'+parentItem.attr('id') + ' .MeetingItemHead .toggleImage').attr('src',portal_url+'/++resource++meeting-styles/arrow_down.png');
                    }


            }).children('.meetingItemActions').click(function(event) {event.stopPropagation();});
    }
$(MeetingItemToggler);
