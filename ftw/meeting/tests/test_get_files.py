from ftw.meeting.testing import FTW_MEETING_INTEGRATION_TESTING
import unittest2 as unittest
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
from plone.app.testing import setRoles, login
from ftw.meeting.interfaces import IMeetingLayer
from zope.interface import directlyProvidedBy, directlyProvides
from DateTime import DateTime

class TestGetFilesView(unittest.TestCase):
    
    layer = FTW_MEETING_INTEGRATION_TESTING


    def test_get_files(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory('Meeting', 'myfolder')
        myfolder = portal['myfolder']
        files = []
        for i in range(3):
            myfolder.invokeFactory('File', 'meeting'+str(i))
            files.append(myfolder['meeting'+str(i)])
        layer = [IMeetingLayer]
        ifaces = layer + list(directlyProvidedBy(self.layer['request']))
        directlyProvides(self.layer['request'], *ifaces) 
        view = myfolder.restrictedTraverse("meeting_view")
        returned_files = view.getFiles()
        self.assertEqual(len(returned_files), 3)
        for i in range(3):
            self.assertEqual(returned_files[i]['url'], 'http://nohost/plone/myfolder/meeting'+str(i))
            self.assertEqual(returned_files[i]['Creator'], 'test_user_1_')