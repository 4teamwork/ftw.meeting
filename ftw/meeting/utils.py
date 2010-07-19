from zope.interface import implements
from interfaces import IResponsibilityInfoGetter
from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName

class ResponsibilityInfos(object):
    """Utiliy which returns a list of dicts
    format: [{'name':'Full Name', 'url':'authors-url'}]
    
    """
    implements(IResponsibilityInfoGetter)
    
    def __call__(self, context, userids=None):
        """
        """
        # we need userids
        if not userids:
            return []
        
        if context is None:
            context = getSite()

        mt = getToolByName(context, 'portal_membership')
        
        users = []
        for userid in userids:
            if userid:
                user = mt.getMemberById(userid)
                users.append({'name': user.getProperty('fullname', ''),
                              'url': '%s/author/%s' % (context.portal_url(), 
                                                       user.id), })
        return users
        