from ftw.builder import Builder
from ftw.builder import create
from ftw.meeting.interfaces import IMeetingLayer
from ftw.meeting.testing import FTW_MEETING_INTEGRATION_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from unittest2 import TestCase
from zope.interface import alsoProvides


class TestMeetingRepresentation(TestCase):

    layer = FTW_MEETING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        request = self.layer['request']
        alsoProvides(request, IMeetingLayer)

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

    def test_meeting_view_get_related_items(self):
        file_ = create(Builder('file'))
        meeting = create(Builder('meeting'))
        meetingitem = create(Builder('meeting item')
                             .having(related_items=file_)
                             .within(meeting))

        meetingview = meeting.restrictedTraverse('@@meeting_view')
        brains = meetingview.get_related_items(meetingitem)
        self.assertEquals([file_], [brain.getObject() for brain in brains])
