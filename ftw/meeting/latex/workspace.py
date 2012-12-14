from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.meeting import _
from ftw.pdfgenerator.interfaces import ILaTeXLayout
from ftw.table import helper
from ftw.workspace.interfaces import IWorkspace
from ftw.workspace.interfaces import IWorkspaceDetailsListingProvider
from zope.component import adapts
from zope.i18n import translate
from zope.interface import Interface
from zope.interface import implements


class EventsListing(object):
    implements(IWorkspaceDetailsListingProvider)
    adapts(IWorkspace, Interface, ILaTeXLayout, Interface)

    template = ViewPageTemplateFile('templates/events_listing.pt')

    def __init__(self, context, request, layout, view):
        self.context = context
        self.request = request
        self.layout = layout
        self.view = view

    def get_sort_key(self):
        return 20

    def get_title(self):
        return translate(_(u'latex_label_events', u'Events'),
                         context=self.request)

    def get_listing(self):
        if len(self._brains()) == 0:
            return None
        else:
            return self.view.convert(self.template())

    def get_items(self):
        acl_users = getToolByName(self.context, 'acl_users')

        for brain in self._brains():
            obj = brain.getObject()

            attendees = []
            for userid in obj.getAttendeesOrUsers():
                user = acl_users.getUserById(userid)
                attendees.append(
                    user and user.getProperty('fullname', userid) or userid)

            yield {
                'title': obj.Title(),
                'start': helper.readable_date(brain, obj.startDate),
                'attendees': ', '.join(attendees),
                }

    def _brains(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        query = {'path': '/'.join(self.context.getPhysicalPath()),
                 'portal_type': ['Meeting', 'Poodle', 'Event'],
                 'sort_on': 'start',
                 'sort_order': 'reverse'}

        return catalog(query)
