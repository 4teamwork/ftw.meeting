from Products.CMFCore.utils import getToolByName
from ftw.meeting.interfaces import IResponsibilityInfoGetter
from zope.app.component.hooks import getSite
from zope.interface import implements


class ResponsibilityInfos(object):
    """Utiliy which returns a list of dicts
    format: [{'name':'Full Name', 'url':'authors-url'}]
    """

    implements(IResponsibilityInfoGetter)

    def __init__(self, context=None):
        if context is None:
            context = getSite()
        self.context = context

    def get_infos(self, userids=None):
        # we need userids
        if not userids:
            return []

        mt = getToolByName(self.context, 'portal_membership')

        users = []
        for userid in userids:
            if userid:
                user = mt.getMemberById(userid)
                users.append({'name': user.getProperty('fullname', ''),
                              'url': '%s/author/%s' % (
                            self.context.portal_url(), user.id), })
        return users
