from ftw.meeting.interfaces import IMeetingItem
from ftw.meeting.latex.layout import MeetingLayout
from ftw.meeting.latex.views import MeetingItemView
from ftw.meeting.testing import LATEX_ZCML_LAYER
from ftw.pdfgenerator.interfaces import IBuilder
from ftw.pdfgenerator.interfaces import ILaTeXView
from ftw.testing import MockTestCase
from mocker import ANY
from zope.component import getMultiAdapter
from zope.interface.verify import verifyClass


class TestMeetingItemView(MockTestCase):

    layer = LATEX_ZCML_LAYER

    def setUp(self):
        super(TestMeetingItemView, self).setUp()
        self.context = self.providing_stub([IMeetingItem])
        self.request = self.stub()
        self.builder = self.providing_stub([IBuilder])
        self.layout = MeetingLayout(self.context, self.request, self.builder)

    def test_component_registered(self):
        self.replay()

        view = getMultiAdapter(
            (self.context, self.request, self.layout), ILaTeXView)

        self.assertEqual(type(view), MeetingItemView)

    def test_implements_interface(self):
        self.replay()

        self.assertTrue(ILaTeXView.implementedBy(MeetingItemView))
        verifyClass(ILaTeXView, MeetingItemView)

    def test_rendering(self):
        self.expect(self.context.Title()).result('Introduction')

        responsibility = self.stub()
        self.expect(self.context.getField('responsibility')).result(
            responsibility)
        self.expect(responsibility.get(self.context)).result('hugo.boss')
        self.expect(responsibility.Vocabulary(self.context)).result(
            responsibility)
        self.expect(responsibility.getValue(ANY)
                    ).result('Hugo Boss')
        self.expect(self.context.getResponsibility()).result(['hugo.boss'])

        self.expect(self.context.getText()).result('agenda <b>item</b> text')
        self.expect(self.context.getConclusion()).result(
            'the <b>conclusion</b>')
        self.expect(self.context.absolute_url()).result('http://nohost/plone/item')
        self.expect(self.context.getRelated_items()).result([
                self.create_dummy(Title=lambda: 'a file',
                                  absolute_url=lambda: '/item/a%20file'),
                self.create_dummy(Title=lambda: 'a file',
                                  absolute_url=lambda: '/item/a-file')])

        self.replay()

        view = getMultiAdapter(
            (self.context, self.request, self.layout), ILaTeXView)

        args = view.get_render_arguments()
        self.assertIn('_', args)
        del args['_']

        self.assertEqual(
            args,
            {'title': 'Introduction',
             'responsibles': ['Hugo Boss'],
             'text': 'agenda \\textbf{item} text',
             'conclusion': 'the \\textbf{conclusion}',
             'relatedItems': [
                    r'\href{/item/a\%20file}{a file\footnote{' +\
                        r'\href{/item/a\%20file}{/""item/""a\%20file}}}',

                    r'\href{/item/a-file}{a file\footnote{' +\
                        r'\href{/item/a-file}{/""item/""a-file}}}']})

        view.render()
