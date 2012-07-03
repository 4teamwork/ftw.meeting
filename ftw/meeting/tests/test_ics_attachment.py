from ftw.meeting.testing import FTW_MEETING_INTEGRATION_TESTING
from ftw.meeting.attachment import ICSAttachmentCreator
import unittest2 as unittest
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
from plone.app.testing import setRoles, login
import DateTime


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
        self.assertEqual("URL:http://nohost/plone/test/meeting" in ics_data, True)
        self.assertEqual("BEGIN:VALARM\r\nTRIGGER:-PT30M\r\nACTION:DISPLAY\r\nDESCRIPTION:Reminder\r\nEND:VALARM" in ics_data, True)