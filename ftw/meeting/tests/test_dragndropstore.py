from ftw.meeting.testing import FTW_MEETING_INTEGRATION_TESTING
import unittest2 as unittest
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
from plone.app.testing import setRoles, login
from ftw.meeting.interfaces import IMeetingLayer
from zope.interface import directlyProvidedBy, directlyProvides
from DateTime import DateTime

class TestDragnDropStorageView(unittest.TestCase):
    
    layer = FTW_MEETING_INTEGRATION_TESTING


    def test_meeting_creation(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory('Meeting', 'myfolder')
        myfolder = portal['myfolder']
        meetings = []
        for i in range(3):
            myfolder.invokeFactory('Meeting Item', 'meeting'+str(i))
            meetings.append(myfolder['meeting'+str(i)])
        self.assertEqual(myfolder.getObjectPosition(meetings[0].id),0)
        self.assertEqual(myfolder.getObjectPosition(meetings[1].id),1)
        self.assertEqual(myfolder.getObjectPosition(meetings[2].id),2)
        uid_string = meetings[0].UID()+','+meetings[2].UID()+','+meetings[1].UID()
        view = myfolder.restrictedTraverse("meetingitem_dnd_saveorder")
        view(uid_string)
        self.assertEqual(myfolder.getObjectPosition(meetings[0].id),0)
        self.assertEqual(myfolder.getObjectPosition(meetings[1].id),2)
        self.assertEqual(myfolder.getObjectPosition(meetings[2].id),1)
