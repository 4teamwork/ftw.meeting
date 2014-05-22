from ftw.builder import Builder
from ftw.builder import create
from ftw.meeting.interfaces import IMeeting
from ftw.meeting.testing import FTW_MEETING_FUNCTIONAL_TESTING
from ftw.meeting.testing import FTW_MEETING_INTEGRATION_TESTING
from ftw.pdfgenerator.interfaces import IPDFAssembler
from ftw.testbrowser.pages import statusmessages
from ftw.testbrowser import browsing
from plone.app.testing import login, setRoles
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
from zope.component import adapts
from zope.component import getMultiAdapter
from zope.interface import implements
from zope.interface import Interface
import unittest2 as unittest


class MockPDFAssembler(object):
    implements(IPDFAssembler)
    adapts(IMeeting, Interface)

    def __init__(self, context, request):
        pass

    def build_pdf(self):
        return "%PDF-1.5\ndummy_pdf"


class TestSaveAsPdfFunctional(unittest.TestCase):

    layer = FTW_MEETING_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        site_manager = self.portal.getSiteManager()
        site_manager.registerAdapter(
            MockPDFAssembler,
            required=(IMeeting, Interface),
            provided=IPDFAssembler)

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

    @browsing
    def test_add_a_new_object_calling_the_view(self, browser):
        meeting = create(Builder('meeting'))
        self.assertTrue(len(self.portal.listFolderContents()) is 1)

        browser.login().visit(meeting, view="save_as_pdf")

        self.assertTrue(len(self.portal.listFolderContents()) is 2)

    @browsing
    def test_portalmessage_if_creation_was_successfull(self, browser):
        meeting = create(Builder('meeting'))

        browser.login().visit(meeting, view="save_as_pdf")
        statusmessages.assert_message('PDF creation was successfully.')

    def tearDown(self):
        site_manager = self.portal.getSiteManager()
        site_manager.unregisterAdapter(MockPDFAssembler)


class TestSaveAsPdfIntegration(unittest.TestCase):

    layer = FTW_MEETING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        site_manager = self.portal.getSiteManager()
        site_manager.registerAdapter(
            MockPDFAssembler,
            required=(IMeeting, Interface),
            provided=IPDFAssembler)

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

    def test_create_object_with_a_pdf_in_same_folder_as_a_meeting(self):
        meeting = create(Builder('meeting'))

        view = getMultiAdapter((meeting, self.request), name="save_as_pdf")
        pdf = view.save_as_pdf()
        self.assertEqual('application/pdf', pdf.getFile().content_type)

    def test_pdf_filename_is_title_of_meeting(self):
        meeting = create(Builder('meeting').titled('J\xc3\xa4mes'))

        view = getMultiAdapter((meeting, self.request), name="save_as_pdf")
        pdf = view.save_as_pdf()
        self.assertEqual('J\xc3\xa4mes.pdf', pdf.getFile().filename)

    def test_file_object_filename_is_title_of_meeting(self):
        meeting = create(Builder('meeting').titled('J\xc3\xa4mes'))

        view = getMultiAdapter((meeting, self.request), name="save_as_pdf")
        pdf = view.save_as_pdf()
        self.assertEqual('J\xc3\xa4mes.pdf', pdf.getFilename())

    def test_title_of_file_object_is_title_of_meeting(self):
        meeting = create(Builder('meeting').titled('J\xc3\xa4mes'))

        view = getMultiAdapter((meeting, self.request), name="save_as_pdf")
        pdf = view.save_as_pdf()
        self.assertEqual('J\xc3\xa4mes', pdf.Title())

    def test_id_of_file_is_id_of_meeting_with_prefix_pdf(self):
        meeting = create(Builder('meeting').titled('james'))

        view = getMultiAdapter((meeting, self.request), name="save_as_pdf")
        view.PREFIX = "PDF_"
        pdf = view.save_as_pdf()
        self.assertEqual('PDF_james', pdf.getId())

    def test_referencing_created_pdf(self):
        meeting = create(Builder('meeting'))

        view = getMultiAdapter((meeting, self.request), name="save_as_pdf")
        pdf = view.save_as_pdf()
        self.assertEqual([pdf], meeting.getRelated_items())

    def test_add_a_new_reference_for_each_call(self):
        meeting = create(Builder('meeting'))

        view = getMultiAdapter((meeting, self.request), name="save_as_pdf")
        pdf_1 = view.save_as_pdf()
        pdf_2 = view.save_as_pdf()

        self.assertIn(pdf_1, meeting.getRelated_items())
        self.assertIn(pdf_2, meeting.getRelated_items())

    def tearDown(self):
        site_manager = self.portal.getSiteManager()
        site_manager.unregisterAdapter(MockPDFAssembler)
