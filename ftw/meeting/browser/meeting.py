from Products.Five.browser import BrowserView
from plone.app.layout.viewlets.content import ContentRelatedItems


class MeetingView(BrowserView):
    """Meeting View
    """
    def getFiles(self):
        context = self.context.aq_inner
        query = dict(
            portal_type=['File', ],
            sort_on='effective',
            sort_order='descending',
            )

        raw = context.getFolderContents(contentFilter=query)

        return [dict(title=b.Title,
                     url=b.getURL(),
                     Description=b.Description,
                     Creator=b.Creator,
                     icon='%s/%s' % (context.portal_url(), b.getIcon))
                for b in raw]


    def get_related_items(self, obj):
        brains = ContentRelatedItems(obj, obj.REQUEST, self).related_items()
        return brains
