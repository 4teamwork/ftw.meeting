from ftw.meeting.attachment import ICSAttachmentCreator
from ftw.meeting.testing import FTW_MEETING_INTEGRATION_TESTING
from plone.app.testing import setRoles, login
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
import DateTime
import unittest2 as unittest


class TestIcsAttachmentView(unittest.TestCase):

    layer = FTW_MEETING_INTEGRATION_TESTING

    def test_ics_attachment(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory('Folder', 'test')
        test = portal['test']
        test.invokeFactory('Meeting', 'meeting')
        meeting = test['meeting']
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
