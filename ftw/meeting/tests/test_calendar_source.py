from DateTime import DateTime
from ftw.builder import Builder
from ftw.builder import create
from ftw.meeting.interfaces import IMeetingLayer
from ftw.meeting.testing import FTW_MEETING_INTEGRATION_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from unittest2 import TestCase
from zope.component import getMultiAdapter
from zope.interface import alsoProvides


class TestCalendarSource(TestCase):

    layer = FTW_MEETING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        self.user = create(Builder('user'))
        setRoles(self.portal, self.user.getId(), ['Manager'])
        login(self.portal, self.user.getId())

        alsoProvides(self.layer['request'], IMeetingLayer)

    def test_customized_json_source_adapter(self):
        adapter = getMultiAdapter((self.portal, self.portal.REQUEST),
                                  name='ftw_calendar_source')

        self.meeting = create(Builder('meeting')
                              .having(head_of_meeting=self.user.getId(),
                                      meeting_type=u'meeting',
                                      start_date=DateTime('08/20/2010 08:00'),
                                      end_date=DateTime('08/20/2010 10:00')))

        brain = adapter.get_event_brains()[0]
        source_dict = adapter.generate_source_dict_from_brain(brain)

        self.assertIn('attendee',
                      source_dict['className'])
