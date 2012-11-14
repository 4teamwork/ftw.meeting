from ftw.meeting.interfaces import IMeeting
from ftw.meeting.latex.layout import MeetingLayout
from ftw.meeting.testing import LATEX_ZCML_LAYER
from ftw.pdfgenerator.interfaces import IBuilder
from ftw.pdfgenerator.interfaces import ILaTeXLayout
from ftw.pdfgenerator.tests import test_customizable_layout
from ftw.testing import MockTestCase
from zope.component import getMultiAdapter


class TestMeetingLayout(test_customizable_layout.TestCustomizableLayout,
                        MockTestCase):
    layout_class = MeetingLayout

    layer = LATEX_ZCML_LAYER

    def setUp(self):
        test_customizable_layout.TestCustomizableLayout.setUp(
            self,
            context=self.create_dummy(getLanguage=lambda: 'de-ch'))
        MockTestCase.setUp(self)

    def tearDown(self):
        MockTestCase.setUp(self)
        test_customizable_layout.TestCustomizableLayout.setUp(self)

    def test_component_registered(self):
        context = self.providing_stub([IMeeting])
        request = self.create_dummy()
        builder = self.providing_stub([IBuilder])

        self.replay()

        layout = getMultiAdapter((context, request, builder), ILaTeXLayout)

        self.assertEqual(type(layout), self.layout_class)

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
