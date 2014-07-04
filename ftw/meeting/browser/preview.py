from ftw.meeting.browser.meeting import MeetingView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class MeetingPreview(MeetingView):

    template = ViewPageTemplateFile('preview.pt')

    def __call__(self):
        return self.template()
