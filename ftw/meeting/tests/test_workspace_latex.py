from DateTime import DateTime
from ftw.meeting.latex.workspace import EventsListing
from ftw.meeting.testing import LATEX_ZCML_LAYER
from ftw.pdfgenerator.interfaces import IHTML2LaTeXConverter
from ftw.pdfgenerator.interfaces import ILaTeXLayout
from ftw.pdfgenerator.interfaces import ILaTeXView
from ftw.testing import MockTestCase
from ftw.workspace.interfaces import IWorkspace
from ftw.workspace.interfaces import IWorkspaceDetailsListingProvider
from mocker import ANY
from zope.component import getMultiAdapter


class TestEventsListing(MockTestCase):

    layer = LATEX_ZCML_LAYER

    def setUp(self):
        MockTestCase.setUp(self)

        self.context = self.providing_stub(IWorkspace)
        self.expect(self.context.getPhysicalPath()).result(
            ['', 'path', 'to', 'workspace'])

        self.layout = self.stub_interface(ILaTeXLayout)
        self.expect(self.layout.use_package(ANY))

        self.view = self.stub_interface(ILaTeXView)

        def convert(*args, **kwargs):
            return getMultiAdapter(
                (self.context, self.request, self.layout),
                IHTML2LaTeXConverter).convert(*args, **kwargs)

        self.expect(self.view.convert).result(convert)

        self.response = self.stub()
        self.expect(self.response.getHeader(ANY))
        self.expect(self.response.setHeader(ANY, ANY))
        self.request = self.create_dummy(debug=True,
                                         response=self.response)

        portal_catalog = self.stub()
        self.mock_tool(portal_catalog, 'portal_catalog')

        self.meetings = []
        def get_catalog_result(query):
            for obj in self.meetings:
                yield self.create_dummy(getObject=lambda x=obj: obj)

        self.expect(portal_catalog(
                {'path': '/path/to/workspace',
                 'portal_type': ['Meeting',
                                 'Poodle',
                                 'Event'],
                 'sort_on': 'start',
                 'sort_order': 'reverse'})).call(get_catalog_result)

        self.acl_users = self.stub()
        self.mock_tool(self.acl_users, 'acl_users')
        self._mock_user('john.doe', 'John Doe')

    def _mock_user(self, userid, fullname):
        self.expect(self.acl_users.getUserById(userid).getProperty(
                'fullname', userid)).result(fullname)

    def test_component_is_registered(self):
        self.replay()
        listing = getMultiAdapter(
            (self.context, self.request, self.layout, self.view),
            IWorkspaceDetailsListingProvider,
            name='events-listing')

        self.assertEqual(type(listing), EventsListing)

    def test_implements_interface(self):
        self.replay()
        self.assertTrue(IWorkspaceDetailsListingProvider.implementedBy(
                EventsListing))

    def test_get_sort_key(self):
        self.replay()
        listing = getMultiAdapter(
            (self.context, self.request, self.layout, self.view),
            IWorkspaceDetailsListingProvider,
            name='events-listing')
        self.assertEqual(listing.get_sort_key(), 20)

    def test_get_title(self):
        self.replay()
        listing = getMultiAdapter(
            (self.context, self.request, self.layout, self.view),
            IWorkspaceDetailsListingProvider,
            name='events-listing')
        self.assertEqual(listing.get_title(), 'Events')

    def test_get_items(self):
        self._mock_user('hugo.boss', 'Hugo Boss')

        self.meetings = [
            self.create_dummy(
                Title=lambda: 'foo',
                startDate=DateTime('05/23/2010'),
                getAttendeesOrUsers=lambda: ['john.doe', 'hugo.boss'])]

        self.replay()
        listing = getMultiAdapter(
            (self.context, self.request, self.layout, self.view),
            IWorkspaceDetailsListingProvider,
            name='events-listing')

        self.assertEqual(list(listing.get_items()), [
                {'title': 'foo',
                 'start': '23.05.2010',
                 'attendees': 'John Doe, Hugo Boss'}])

    def test_rendering(self):
        self._mock_user('hugo.boss', 'Hugo Boss')
        self._mock_user('jane.doe', 'Jane Doe')

        self.meetings = [
            self.create_dummy(
                Title=lambda: 'first meeting',
                startDate=DateTime('05/23/2010'),
                getAttendeesOrUsers=lambda: ['john.doe', 'hugo.boss']),

            self.create_dummy(
                Title=lambda: 'second meeting',
                startDate=DateTime('06/12/2010'),
                getAttendeesOrUsers=lambda: ['jane.doe', 'john.doe'])]

        self.replay()
        listing = getMultiAdapter(
            (self.context, self.request, self.layout, self.view),
            IWorkspaceDetailsListingProvider,
            name='events-listing')

        latex = listing.get_listing()
        self.assertIn(r'\begin{tabular}', latex)

        self.assertIn(r'23.05.2010', latex)
        self.assertIn(r'first meeting', latex)
        self.assertIn(r'John Doe, Hugo Boss', latex)

        self.assertIn(r'12.06.2010', latex)
        self.assertIn(r'second meeting', latex)
        self.assertIn(r'Jane Doe, John Doe', latex)
