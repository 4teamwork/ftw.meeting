from Acquisition import aq_inner, aq_parent
from DateTime import DateTime
from ftw.meeting.interfaces import IMeetingLayer
from ftw.meeting.testing import FTW_MEETING_INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
from plone.app.testing import setRoles, login, logout
from zope.interface import directlyProvidedBy, directlyProvides
import unittest2 as unittest

class TestCreateMeetingView(unittest.TestCase):

    layer = FTW_MEETING_INTEGRATION_TESTING

    def setUp(self):
        super(TestCreateMeetingView, self).setUp()
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory('Folder', 'myfolder')
        self.folder = portal['myfolder']

    def tearDown(self):
        super(TestCreateMeetingView, self).tearDown()
        parent = aq_parent(aq_inner(self.folder))
        parent.manage_delObjects([self.folder.getId()])
        logout()

    def test_meeting_creation(self):
        self.folder.invokeFactory('Poodle', 'testpoodle')
        poodle = self.folder['testpoodle']
        data = {'dates': ['08.07.2012', '09.08.2012'],
                'ids': ['8729834410356338367', '7414187398453506251'],
                'users':{'testi.testmann':{'8729834410356338367': True}}}
        date = [{'date':'08.07.2012', 'duration':'11:00-12:00'}]
        poodle.setDates(date)
        poodle.setPoodleData(data)

        layer = [IMeetingLayer]
        ifaces = layer + list(directlyProvidedBy(self.layer['request']))
        directlyProvides(self.layer['request'], *ifaces)
        poodle.restrictedTraverse('create_meeting_from_poodle')(data['ids'][0])

        created_event = self.folder.listFolderContents(
            dict(portal_type='Meeting'))[0]

        self.assertEqual(created_event.start(),
                         DateTime('2012/08/07 11:00:00 GMT+2'))
        self.assertEqual(created_event.end(),
                         DateTime('2012/08/07 12:00:00 GMT+2'))
        self.assertEqual(created_event.attendees,
                         ({'contact': 'testi.testmann', 'present': ''},))
