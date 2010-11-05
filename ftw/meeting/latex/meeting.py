from Products.CMFCore.utils import getToolByName
from plonegov.pdflatex.browser.converter import LatexCTConverter


class MeetingLatexConverter(LatexCTConverter):
    
    def __call__(self, context, view):
        super(MeetingLatexConverter, self).__call__(context, view)
        
        latex = []
        latex.append(r'\section*{%s}' % view.convert(context.Title()))
        latex.append(r'\begin{tabular}{|p{0.3\textwidth}|p{0.7\textwidth}|}')
        latex.append(self.get_row(
            'Start-Datum',
            context.toLocalizedTime(context.start())))
        latex.append(self.get_row(
            'Start-Zeit',
            context.toLocalizedTime(context.start(), time_only=1)))
        latex.append(self.get_row(
            'End-Datum',
            context.toLocalizedTime(context.end())))
        latex.append(self.get_row(
            'End-Zeit',
            context.toLocalizedTime(context.end(), time_only=1)))
        latex.append(self.get_row('Verantwortliche',
                                  self.get_latex_responsibility()))
        latex.append(self.get_row('Beschreibung', context.Description()))
        latex.append(r'\hline \end{tabular}')
        return '\n'.join(latex)

    def get_row(self, title, value):
        return r'\hline \textbf{%s} & %s\\' % (title, value)

    def get_latex_responsibility(self):
        result = []
        for term in self.context.getResponsibility():
            userid = term['contact']
            mt = getToolByName(self, 'portal_membership')
            user = mt.getMemberById(userid)
            fullname = '-'
            if user:
                fullname = user.getProperty('fullname', '')
                if not fullname:
                    fullname = userid
            else:
                catalog = getToolByName(self, 'portal_catalog')
                brains = catalog(dict(UID=userid))
                if len(brains):
                    brain = brains[0]
                    fullname = brain.Title
            result.append(self.view.convert(fullname))
        return '\\newline '.join(result)
