from Products.Five.browser import BrowserView
from plone.memoize import ram
from zope.component import getMultiAdapter

def _get_contents_key(method, self):
    return [b.modified for b in self.context.getFolderContents()]

class MeetingUpdate(BrowserView):
    def __call__(self):
        meetings = map(lambda x: x.getObject(), self.context.portal_catalog(Type='Meeting'))
        for meeting in meetings:
            poodledata = meeting.getPoodleData()
            if not poodledata.has_key('ids'):
                meeting.updatePoodleData()

class MeetingView(BrowserView):

    @ram.cache(_get_contents_key)
    def getFiles(self):
        context = self.context.aq_inner
        query = dict(
            portal_type = ['File',],
            sort_on = 'effective',
            sort_order = 'descending',
            )
        raw = context.getFolderContents(contentFilter=query)
        return [dict(title=b.Title,
                     url = b.getURL(),
                     Description=b.Description,
                     Creator=b.Creator,
                     icon = '%s/%s'%(context.portal_url(),b.getIcon))
                for b in raw]


    def renderPoodleTable(self, poodle):
        view = getMultiAdapter((poodle, poodle.REQUEST), name=u'ftw_poodle_table')
        return view()


