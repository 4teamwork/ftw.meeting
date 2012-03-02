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
