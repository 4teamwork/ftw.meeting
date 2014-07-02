from DateTime import DateTime
from ftw.builder import Builder
from ftw.builder import create
from ftw.meeting.testing import FTW_MEETING_FUNCTIONAL_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from unittest2 import TestCase
from ftw.testbrowser import browsing, browser


class TestTaskListing(TestCase):

    layer = FTW_MEETING_FUNCTIONAL_TESTING

    def setUp(self):

        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        self.user1 = create(Builder('user'))
        self.meeting = create(Builder('meeting')
                         .titled('THE event')
                         .having(start_date=DateTime('08/20/2010 08:00'),
                                 end_date=DateTime('08/20/2010 10:00'),
                                 head_of_meeting=self.user1.getId()))

        self.meetingitem = create(Builder(
                                  'meeting item').within(
                                  self.meeting).titled('Stuff'))

    @browsing
    def test_meeting_preview_table(self, browser):
        page = browser.login().visit(self.meeting, view="meeting_preview")
        self.assertEqual([
                         ['Title', 'THE event'],
                         ['Date', '20.08.2010'],
                         ['Duration', '08:00 - 10:00'],
                         ['Meeting Items', 'Stuff'],
                         ], page.css('.MeetingPreview').first.lists())
