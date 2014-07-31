from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView


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
        context = aq_inner(obj)
        res = ()

        catalog = getToolByName(context, 'portal_catalog')
        related = context.getRawRelated_items()
        if not related:
            return ()
        brains = catalog(UID=related)
        if brains:
            # build a position dict by iterating over the items once
            positions = dict([(v, i) for (i, v) in enumerate(related)])
            # We need to keep the ordering intact
            res = list(brains)

            def _key(brain):
                return positions.get(brain.UID, -1)
            res.sort(key=_key)
        return res
