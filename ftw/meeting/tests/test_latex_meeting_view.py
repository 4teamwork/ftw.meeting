from DateTime import DateTime
from Products.CMFPlone.i18nl10n import ulocalized_time
from ftw.meeting.interfaces import IMeeting
from ftw.meeting.latex.layout import MeetingLayout
from ftw.meeting.latex.views import MeetingView
from ftw.meeting.testing import LATEX_ZCML_LAYER
from ftw.pdfgenerator.interfaces import IBuilder
from ftw.pdfgenerator.interfaces import ILaTeXView
from ftw.testing import MockTestCase
from mocker import ANY
from zope.component import getMultiAdapter
from zope.interface.verify import verifyClass


class TranslationServiceStub(object):

    def __init__(self, context):
        self.context = context

    def ulocalized_time(self, *args, **kwargs):
        kwargs['context'] = self.context
        return ulocalized_time(*args, **kwargs)


class TestMeetingView(MockTestCase):

    layer = LATEX_ZCML_LAYER

    def setUp(self):
        self.context = self.providing_stub([IMeeting])
        self.request = self.stub()
        self.builder = self.providing_stub([IBuilder])
        self.layout = MeetingLayout(self.context, self.request, self.builder)

        self.expect(self.context.REQUEST).result(self.request)
        self.expect(self.request.get('paths', None)).result(None)

        self.translation_service = TranslationServiceStub(self.context)
        self.mock_tool(self.translation_service, 'translation_service')

        self.portal_properties = self.stub()
        self.mock_tool(self.portal_properties, 'portal_properties')
        self.expect(self.portal_properties.site_properties).result(
            self.create_dummy(localLongTimeFormat='%d.%m.%Y %H:%M',
                              localTimeFormat='%d.%m.%Y',
                              localTimeOnlyFormat='%H:%M'))

    def test_component_registered(self):
        self.replay()

        view = getMultiAdapter(
            (self.context, self.request, self.layout), ILaTeXView)

        self.assertEqual(type(view), MeetingView)

    def test_implements_interface(self):
        self.replay()

        self.assertTrue(ILaTeXView.implementedBy(MeetingView))
        verifyClass(ILaTeXView, MeetingView)

    def test_get_dates_metadata_same_day(self):
        self.expect(self.context.start_date).result(
            DateTime('04/25/2010 10:00'))
        self.expect(self.context.end_date).result(
            DateTime('04/25/2010 13:00'))

        self.replay()

        view = getMultiAdapter(
            (self.context, self.request, self.layout), ILaTeXView)

        self.assertEqual(
            view.get_dates_metadata(),

            [(u'latex_date', '25.04.2010'),
             (u'latex_duration', '10:00\,--\,13:00')])

    def test_get_dates_metadata_different_day(self):
        self.expect(self.context.start_date).result(
            DateTime('08/20/2010 08:00'))
        self.expect(self.context.end_date).result(
            DateTime('08/22/2010 16:00'))

        self.replay()

        view = getMultiAdapter(
            (self.context, self.request, self.layout), ILaTeXView)

        self.assertEqual(
            view.get_dates_metadata(),

            [(u'latex_start', '20.08.2010 08:00'),
             (u'latex_end', '22.08.2010 16:00')])

    def test_event(self):
        self.expect(self.context.getMeeting_type()).result('event')
        self.expect(self.context.Title()).result('THE event')
        self.expect(self.context.listFolderContents()).result([])
        self.expect(self.context.start_date).result(
            DateTime('08/20/2010 08:00'))
        self.expect(self.context.end_date).result(
            DateTime('08/22/2010 16:00'))
        self.expect(self.context.getField('location').get(
                self.context)).result('Switzerland')
        self.expect(self.context.getField('location').Vocabulary(
                self.context)).result(None)

        self.replay()

        view = getMultiAdapter(
            (self.context, self.request, self.layout), ILaTeXView)

        args = view.get_render_arguments()
        self.assertIn('_', args)
        del args['_']

        self.assertEqual(
            args,
            {'latex_content': '',
             'title': 'THE event',
             'meetingForm': '',
             'metadata': [
                    (u'Start', '20.08.2010 08:00'),
                    (u'End', '22.08.2010 16:00'),
                    (u'Location', 'Switzerland')],
             'meetingItems': None})

        view.render()

    def test_meeting(self):
        self.expect(self.context.getMeeting_type()).result('meeting')
        self.expect(self.context.Title()).result('THE meeting')
        self.expect(self.context.listFolderContents()).result([])
        self.expect(self.context.start_date).result(
            DateTime('08/20/2010 08:00'))
        self.expect(self.context.end_date).result(
            DateTime('08/22/2010 16:00'))

        def mock_field(fieldname, value):
            self.expect(self.context.getField(fieldname).get(
                    self.context)).result(value)
            self.expect(self.context.getField(fieldname).Vocabulary(
                    self.context)).result(None)

        mock_field('location', 'Bern')
        mock_field('head_of_meeting', 'John Doe')
        mock_field('recording_secretary', 'Hugo Boss')
        mock_field('meeting_form', 'Protocol')

        self.expect(self.context.getAttendeesVocabulary().getValue(
                'hugo.boss')).result('Hugo Boss')
        self.expect(self.context.getAttendeesVocabulary().getValue(
                'john.doe')).result('John Doe')

        self.expect(self.context.getPresentOptions().getValue(
                'present')).result('present')

        self.expect(self.context.getAttendees()).result([
                {'contact': 'hugo.boss',
                 'present': 'present'},
                {'contact': 'john.doe',
                 'present': 'present'},
            ])

        self.expect(self.context.getFolderContents(
                contentFilter=ANY)).result([
                self.create_dummy(Title='foo'),
                self.create_dummy(Title='bar')])

        self.replay()

        view = getMultiAdapter(
            (self.context, self.request, self.layout), ILaTeXView)

        args = view.get_render_arguments()
        self.assertIn('_', args)
        del args['_']

        self.assertEqual(
            args,
            {'latex_content': '',
             'title': 'THE meeting',
             'meetingForm': 'Protocol',
             'metadata': [
                    (u'Start', '20.08.2010 08:00'),
                    (u'End', '22.08.2010 16:00'),
                    (u'Location', 'Bern'),
                    (u'Head of Meeting', 'John Doe'),
                    (u'Recording Secretary', 'Hugo Boss'),
                    ('', ''),
                    (u'Attendees', 'Hugo Boss, present \\newline ' + \
                         'John Doe, present'),
                    ('', '')],
             'meetingItems': ['foo', 'bar']})

        view.render()
