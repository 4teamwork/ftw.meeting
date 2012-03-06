from ftw.meeting.interfaces import IMeeting
from ftw.meeting.latex.layout import MeetingLayout
from ftw.meeting.testing import LATEX_ZCML_LAYER
from ftw.pdfgenerator.interfaces import IBuilder
from ftw.pdfgenerator.interfaces import ILaTeXLayout
from ftw.testing import MockTestCase
from zope.component import getMultiAdapter
from zope.interface.verify import verifyClass


class TestMeetingLayout(MockTestCase):

    layer = LATEX_ZCML_LAYER

    def test_component_registered(self):
        context = self.providing_stub([IMeeting])
        request = self.create_dummy()
        builder = self.providing_stub([IBuilder])

        self.replay()

        layout = getMultiAdapter((context, request, builder), ILaTeXLayout)

        self.assertEqual(type(layout), MeetingLayout)

    def test_implements_interface(self):
        self.assertTrue(ILaTeXLayout.implementedBy(MeetingLayout))
        verifyClass(ILaTeXLayout, MeetingLayout)

    def test_layout_renders(self):
        context = self.providing_stub([IMeeting])
        self.expect(context.getLanguage).result(lambda: 'de-ch')
        request = self.create_dummy()
        builder = self.providing_stub([IBuilder])

        self.replay()

        layout = getMultiAdapter((context, request, builder), ILaTeXLayout)
        latex = layout.render_latex('CONTENT LATEX')

        self.assertIn('CONTENT LATEX', latex)
        self.assertIn(r'\usepackage[ngerman]{babel}', latex)
