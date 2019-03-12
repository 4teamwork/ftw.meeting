from ftw.builder import Builder
from ftw.builder import create
from ftw.meeting.attachment import ICSAttachmentCreator
from ftw.meeting.testing import FTW_MEETING_INTEGRATION_TESTING
from plone.app.testing import setRoles, login
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
import DateTime
import unittest2 as unittest


class TestIcsAttachmentView(unittest.TestCase):

    layer = FTW_MEETING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Folder', 'test')
        self.test = self.portal['test']

    def test_ics_attachment(self):
        self.test.invokeFactory('Meeting', 'meeting')
        meeting = self.test['meeting']
        meeting.title = "TheMeeting"
        meeting.start_date = DateTime.DateTime()
        meeting.end_date = meeting.start_date + 1
        creator = ICSAttachmentCreator(meeting)
        ics = creator(meeting)
        ics_data = ics[0][0].read()
        self.assertEqual("SUMMARY:TheMeeting" in ics_data, True)
        self.assertIn("URL:http://nohost/plone/test/meeting", ics_data)
        self.assertIn("BEGIN:VALARM\r\nTRIGGER:-PT30M\r\nACTION:DISPLAY\r\nDESCRIPTION:Reminder\r\nEND:VALARM",
                      ics_data)

    def test_attendee_email_address_in_ics(self):
        user = create(Builder('user').named('User', 'Test')
                      .with_userid('test.user')
                      .having(email='test@example.com'))
        meeting = create(Builder('meeting')
                         .having(attendees=[{'contact': user.getId(),
                                             'present': 'present'}],
                                 start_date=DateTime.DateTime(),
                                 end_date=DateTime.DateTime() + 10))

        ics = ICSAttachmentCreator(meeting)(meeting)
        ics_data = ics[0][0].read()
        self.assertIn('INDIVIDUAL:test@example.com', ics_data)
