from Products.CMFCore.utils import getToolByName
from ftw.meeting.interfaces import IResponsibilityInfoGetter
from zope.component.hooks import getSite
from zope.interface import implements


def vformat(s):
    # return string with escaped commas and semicolons
    return s.strip().replace(',','\,').replace(';','\;')


def get_memberdata(userid):
    """ Returns the name and the email address of a member.
    The userid can be a email address (for members) or a UID (for contacts)
    """
    context = getSite()
    mt = getToolByName(context, 'portal_membership')
    member = mt.getMemberById(userid)
    if member:
        return (member.getProperty('fullname', member.id),
                member.getProperty('email', userid))
    else:
        catalog = getToolByName(context, 'portal_catalog')
        brains = catalog(UID=userid)
        if len(brains) == 1:
            return (brains[0].Title, brains[0].getObject().getEmail())
    return (userid, userid)


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
