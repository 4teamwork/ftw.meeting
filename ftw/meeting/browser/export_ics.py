from plone.memoize import ram
from Products.ATContentTypes.lib import calendarsupport as cs
from Products.ATContentTypes.browser.calendar import CalendarView, cachekey


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
                value += 'ATTENDEE;CN="%s";CUTYPE=INDIVIDUAL:%s\n' % (
                    info.decode('utf8'),
                    attendee['contact'])
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
            data += '\n'.join(lines)

        data += cs.ICS_FOOTER
        return data
