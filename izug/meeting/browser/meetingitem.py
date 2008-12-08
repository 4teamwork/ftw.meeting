from plonegov.pdflatex.browser.converter import LatexCTConverter

class MeetingItemLatexConverter(LatexCTConverter):

    def getDisplayListValue(self, object, fieldname):
        context = object.aq_inner
        field = context.getField(fieldname)
        vocab = field.Vocabulary(context)
        value = field.get(context)
        return context.displayValue(vocab, value)
    
    def __call__(self, context, view):
        self.view = view
        latex = ''
        latex_title = self.view.convert(context.pretty_title_or_id())
        latex_responsibility = self.getDisplayListValue(context, 'responsibility')
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
