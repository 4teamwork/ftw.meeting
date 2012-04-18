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
                value+='ATTENDEE;CN="%s";CUTYPE=INDIVIDUAL:%s\n' % (
                    voc.getValue(attendee['contact']).decode('utf8'),
                    attendee['contact'])
            return value.encode('utf8')
        return ''


    @ram.cache(cachekey)
    def feeddata(self):
        context = self.context
        data = cs.ICS_HEADER % dict(prodid=cs.PRODID)
        data += 'X-WR-CALNAME:%s\n' % context.Title()
        data += 'X-WR-CALDESC:%s\n' % context.Description()
        for brain in self.events:
            lines = brain.getObject().getICal().split('\n')
            lines.insert(1, self.attendees(brain))
            data += '\n'.join(lines)

        data += cs.ICS_FOOTER
        return data
