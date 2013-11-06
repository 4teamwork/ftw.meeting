from DateTime import DateTime
from ftw.builder import Builder
from ftw.builder import create
from ftw.meeting.latex.views import get_value_from_vocab
from ftw.meeting.testing import FTW_MEETING_INTEGRATION_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from unittest2 import TestCase


class TestCreateMeetingView(TestCase):

    layer = FTW_MEETING_INTEGRATION_TESTING

    def setUp(self):
        super(TestCreateMeetingView, self).setUp()
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

    def test_meetingview_get_value_from_vocab(self):
        user1 = create(Builder('user'))
        meeting = create(Builder('meeting')
                         .titled('Meeting')
                         .having(start_date=DateTime('08/20/2010 08:00'),
                                 end_date=DateTime('08/20/2010 10:00'),
                                 head_of_meeting=user1.getId()))

        vocab = meeting.getField('head_of_meeting').Vocabulary(meeting)
        self.assertEquals(user1.getProperty('fullname'),
                          get_value_from_vocab(vocab, user1.getId()))

        # Edge case, currently not in use in this package
        vocab = meeting.getAttendeesVocabulary()

        attendees = ', '.join((user1.getProperty('fullname'),
                               TEST_USER_NAME))
        self.assertEquals(attendees, get_value_from_vocab(
            vocab,
            (user1.getId(), TEST_USER_NAME)))
