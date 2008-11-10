import re

from zope.component import getMultiAdapter

from plonegov.pdflatex.browser.converter import LatexCTConverter
from plonegov.pdflatex.converter import html2latex

class MeetingItemLatexConverter(LatexCTConverter):

    def __call__(self, context, view):
        plone_view = getMultiAdapter((self.context, self.request), name=u'plone')
        self.view = view
        latex = ''
        latex_title = self.view.convert(context.pretty_title_or_id())
        latex_responsibility = self.view.convert(context.responsibility)
        latex_meetingitem_type = self.view.convert(context.meetingitem_type)
        latex += '\n'
        latex += r'\vspace{0.5cm}'
        latex += '\n'
        latex += r'\meetingitemheader'
        latex += '\n'
        latex += r'\meetingitem{%s}{%s}' % (latex_title, latex_responsibility)
        latex += '\n'
        latex_text = self.view.convert(context.getText())
        latex_conclusion = self.view.convert(context.getConclusion())
        latex += r'\meetingitemtextblock{%s}{%s}' % ('Text', latex_text)
        latex += r'\meetingitemtextblock{%s}{%s}' % ('Conclusion', latex_conclusion)
        latex += '\n'
        return latex
