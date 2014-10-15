from ftw.calendar.browser.calendarupdateview import CalendarJSONSource


class MeetingCalendarJSONSource(CalendarJSONSource):

    def generate_source_dict_from_brain(self, brain):
        output = super(MeetingCalendarJSONSource,
                       self).generate_source_dict_from_brain(brain)

        if brain.Type == 'Meeting' and \
           self.memberid in brain.getAttendeesOrUsers:

            output['className'] += ' attendee'

        return output
