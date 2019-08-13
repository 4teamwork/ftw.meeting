from Products.ATContentTypes.browser.calendar import CalendarView, cachekey
from Products.ATContentTypes.lib import calendarsupport as cs
from plone import api
from plone.memoize import ram


class ExportICS(CalendarView):

    def attendees(self, brain):
        """Returns the attendees prepared for export.
        """
        obj = brain.getObject()
        attendees = obj.getAttendees()
        if attendees:
            voc = self.context.getAttendeesVocabulary()
            value = ''
            for attendee in attendees:
                # getValue returns None if user does not exists
                info = voc.getValue(attendee['contact'])
                if not info:
                    continue

                user = api.user.get(userid=attendee['contact'])
                value += 'ATTENDEE;CN="%s";CUTYPE=INDIVIDUAL:%s\n' % (
                    info.decode('utf8'),
                    user.getProperty('email'))
            return value.encode('utf8')
        return ''

    @ram.cache(cachekey)
    def feeddata(self):
        data = cs.ICS_HEADER % dict(prodid=cs.PRODID)
        # Enabling two lines below results in always creating
        # new calendars in outlook
        # data += 'X-WR-CALNAME:%s\n' % self.context.Title()
        # data += 'X-WR-CALDESC:%s\n' % self.context.Description()
        for brain in self.events:
            lines = brain.getObject().getICal().split('\n')
            lines.insert(1, self.attendees(brain))
            # add organizer of event (head_of_meeting) if there is one
            name_and_email = self.get_name_and_email_of_head_of_meeting(brain)
            if name_and_email:
                head_of_meeting_name = name_and_email[0]
                head_of_meeting_email = name_and_email[1]
                lines.insert(1, 'ORGANIZER;CN={}:MAILTO:{}'.format(
                    head_of_meeting_name, head_of_meeting_email))
            data += '\n'.join(lines)

        data += cs.ICS_FOOTER
        return data

    @staticmethod
    def get_name_and_email_of_head_of_meeting(brain):
        meeting = brain.getObject()
        if not meeting.head_of_meeting:
            # handle if there isn't any organizer
            return None
        user_id = meeting.head_of_meeting[0]
        user = api.user.get(userid=user_id)
        attendees = meeting.getAttendeesVocabulary()

        return attendees.getValue(user_id), user.getProperty('email')
