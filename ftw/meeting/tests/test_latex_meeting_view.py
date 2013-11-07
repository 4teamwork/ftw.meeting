from DateTime import DateTime
from ftw.builder import Builder
from ftw.builder import create
from ftw.meeting.latex.layout import MeetingLayout
from ftw.meeting.latex.views import get_value_from_vocab
from ftw.meeting.latex.views import MeetingView
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
from zope.interface.verify import verifyClass


class TestMeetingView(TestCase):

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

        view = getMultiAdapter(
            (self.meeting, self.meeting.REQUEST, self.layout), ILaTeXView)

        self.assertEqual(type(view), MeetingView)

    def test_implements_interface(self):
        self.assertTrue(ILaTeXView.implementedBy(MeetingView))
        verifyClass(ILaTeXView, MeetingView)

    def test_get_dates_metadata_same_day(self):
        view = getMultiAdapter(
            (self.meeting, self.meeting.REQUEST, self.layout), ILaTeXView)

        self.assertEqual(
            view.get_dates_metadata(),

            [(u'latex_date', 'Aug 20, 2010'),
             (u'latex_duration', '08:00 AM\,--\,10:00 AM')])

    def test_get_dates_metadata_different_day(self):
        self.meeting.setStart_date(DateTime('08/20/2010 08:00'))
        self.meeting.setEnd_date(DateTime('08/22/2010 16:00'))

        view = getMultiAdapter(
            (self.meeting, self.meeting.REQUEST, self.layout), ILaTeXView)

        self.assertEqual(
            view.get_dates_metadata(),

            [(u'latex_start', 'Aug 20, 2010 08:00 AM'),
             (u'latex_end', 'Aug 22, 2010 04:00 PM')])

    def test_event(self):
        self.meeting.setStart_date(DateTime('08/20/2010 08:00'))
        self.meeting.setEnd_date(DateTime('08/22/2010 16:00'))
        self.meeting.setLocation('Switzerland')

        view = getMultiAdapter(
            (self.meeting, self.meeting.REQUEST, self.layout), ILaTeXView)

        args = view.get_render_arguments()
        self.assertIn('_', args)
        del args['_']

        self.assertEqual(
            args,
            {'latex_content': '',
             'title': 'THE event',
             'meetingForm': '',
             'metadata': [
                    (u'Start', 'Aug 20, 2010 08:00 AM'),
                    (u'End', 'Aug 22, 2010 04:00 PM'),
                    (u'Location', 'Switzerland')],
             'meetingItems': None})

        view.render()

    def test_meeting(self):
        self.meeting.setTitle('THE meeting')
        self.meeting.setMeeting_type('meeting')
        self.meeting.setStart_date(DateTime('08/20/2010 08:00'))
        self.meeting.setEnd_date(DateTime('08/22/2010 16:00'))
        self.meeting.setLocation('Berne')
        self.meeting.setMeeting_form('Protokoll')

        user = create(Builder('user').named('Hugo', 'Boss'))
        self.meeting.setRecording_secretary(user.getId())

        self.meeting.setAttendees([{'contact': user.getId(),
                                   'present': 'present'},
                                  {'contact': self.user1.getId(),
                                   'present': 'present'}])

        create(Builder('meeting item').titled('Foo').within(self.meeting))
        create(Builder('meeting item').titled('Bar').within(self.meeting))

        view = getMultiAdapter(
            (self.meeting, self.meeting.REQUEST, self.layout), ILaTeXView)

        args = view.get_render_arguments()
        self.assertIn('_', args)
        del args['_']

        latex = "\\subsection{Foo}\n\n\n\n\n\n\\subsection{Bar}\n\n\n\n\n"
        self.maxDiff = None
        self.assertEquals(
            args,
            {'latex_content': latex,
             'title': 'THE meeting',
             'meetingForm': 'Protokoll',
             'metadata': [
                    (u'Start', 'Aug 20, 2010 08:00 AM'),
                    (u'End', 'Aug 22, 2010 04:00 PM'),
                    (u'Location', 'Berne'),
                    (u'Head of meeting', 'Doe John'),
                    (u'Recording secretary', 'Boss Hugo'),
                    ('', ''),
                    (u'Attendees', 'Boss Hugo, present \\newline '
                                   'Doe John, present'),
                    ('', '')],
             'meetingItems': ['Foo', 'Bar']})

        view.render()

    def test_meetingview_get_value_from_vocab(self):
        meeting = create(Builder('meeting')
                         .titled('Meeting')
                         .having(start_date=DateTime('08/20/2010 08:00'),
                                 end_date=DateTime('08/20/2010 10:00'),
                                 head_of_meeting=self.user1.getId()))

        vocab = meeting.getField('head_of_meeting').Vocabulary(meeting)
        self.assertEquals(self.user1.getProperty('fullname'),
                          get_value_from_vocab(vocab, self.user1.getId()))

        # Edge case, currently not in use in this package
        vocab = meeting.getAttendeesVocabulary()

        attendees = ', '.join((self.user1.getProperty('fullname'),
                               TEST_USER_NAME))
        self.assertEquals(attendees, get_value_from_vocab(
            vocab,
            (self.user1.getId(), TEST_USER_NAME)))
