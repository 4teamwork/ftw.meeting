from Acquisition import aq_parent, aq_inner
from zope.publisher.browser import BrowserView


class MeetingItemView(BrowserView):

    def __call__(self):
        return self.request.response.redirect(
            aq_parent(aq_inner(self.context)).absolute_url())
