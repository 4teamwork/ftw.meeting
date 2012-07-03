from Acquisition import aq_inner
from StringIO import StringIO


class ICSAttachmentCreator(object):
    """An adapter to add ics-attachments.
    Called by ftw.notificatin.email"""

    def __init__(self, context):
        self.context = aq_inner(context)
        self.request = self.context.REQUEST

    def __call__(self, object_):
        mime_type = "text/calendar"
        attachments = []
        ical_view = object_.restrictedTraverse('export_ics')
        if ical_view:
            ical_view.update()
            ical_view = ical_view.feeddata()
            ical_view = self.set_reminder(ical_view, 30)
            ical_file = StringIO(ical_view)
            ical_attachment = (ical_file, 'ICal.ics', mime_type.split('/'))
            attachments = [ical_attachment, ]

        return attachments

    def set_reminder(self, ical, time_in_past):
        """set the reminder of a ical-object"""

        position = ical.find("END:VEVENT")
        if position < 0:
            return ical

        splitted = []
        splitted.append(ical[:position])
        splitted.append(ical[position:])
        splitted[0] += self.get_valarm(time_in_past)

        return "\r\n".join(splitted)

    def get_valarm(self, time_in_past):
        """create and return the valarm-string"""

        valarm = []
        valarm.append("BEGIN:VALARM")
        valarm.append("TRIGGER:-PT%sM" % time_in_past)
        valarm.append("ACTION:DISPLAY")
        valarm.append("DESCRIPTION:Reminder")
        valarm.append("END:VALARM")

        return "\r\n".join(valarm)
