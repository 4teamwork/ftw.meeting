from DateTime import DateTime
from ftw.builder import Builder
from ftw.builder import create
from ftw.meeting.latex.layout import MeetingLayout
from ftw.meeting.latex.tasklisting import TaskListingLaTeXView
from ftw.meeting.testing import FTW_MEETING_INTEGRATION_TESTING
from ftw.pdfgenerator.interfaces import IBuilderFactory
from ftw.pdfgenerator.interfaces import ILaTeXView
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from unittest2 import TestCase
from zope.component import getMultiAdapter
from zope.component import getUtility


class TestTaskListing(TestCase):

    layer = FTW_MEETING_INTEGRATION_TESTING

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

        # self.builder = self.providing_stub([IBuilder])
        self.builder = getUtility(IBuilderFactory)()
        self.layout = MeetingLayout(self.meeting,
                                    self.meeting.REQUEST,
                                    self.builder)

    def test_component_registered(self):

        adapter = getMultiAdapter(
            (self.meeting, self.meeting.REQUEST, self.layout),
            ILaTeXView,
            name="post-hook")

        self.assertEqual(type(adapter), TaskListingLaTeXView)

    def test__get_meeting_tasks(self):
        task = create(Builder('task'))
        file_ = create(Builder('file'))

        self.meeting.setRelatedItems([task.UID(), file_.UID()])

        adapter = getMultiAdapter(
            (self.meeting, self.meeting.REQUEST, self.layout),
            ILaTeXView,
            name="post-hook")

        self.assertEquals((task, ), tuple(adapter._get_meeting_tasks()))
        self.assertNotIn(file_, tuple(adapter._get_meeting_tasks()))

    def test__get_meeting_item_tasks(self):
        task = create(Builder('task'))
        file_ = create(Builder('file'))

        meetingitem = create(Builder('meeting item').within(self.meeting))

        meetingitem.setRelatedItems([task.UID(), file_.UID()])

        adapter = getMultiAdapter(
            (self.meeting, self.meeting.REQUEST, self.layout),
            ILaTeXView,
            name="post-hook")

        self.assertEquals((task, ), tuple(adapter._get_meeting_item_tasks()))
        self.assertNotIn(file_, tuple(adapter._get_meeting_item_tasks()))
