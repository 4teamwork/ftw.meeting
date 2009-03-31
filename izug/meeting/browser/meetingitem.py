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
        latex = []
        w = lambda *a:[latex.append(x) for x in a]
        w()
        w(r'\meeting{%s}' % self.view.convert(context.pretty_title_or_id()))
        w(r'{%s}' % self.view.convert(context.getText()))
        w(r'{%s}' % self.view.convert(context.getConclusion()))
        w(r'{%s}' % self.view.convert(self.getDisplayListValue(context, 'responsibility')))
        w()
        return '\n'.join(latex)
