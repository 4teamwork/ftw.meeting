from Products.CMFCore.utils import getToolByName
from plonegov.pdflatex.browser.converter import LatexCTConverter


class MeetingLatexConverter(LatexCTConverter):

    def __call__(self, context, view):
        self.controller = view
        return self.getLaTeXBody()

    def getLaTeXBody(self):
        # shortcut for converting html to latex
        conv = self.controller.convert
        context = self.context
        # define a method for easy writing
        latex = []

        # traktanden
        traktanden = []
        if len(context.getChildNodes()):
            for brain in context.getChildNodes():
                responsibility = [{'contact': t} for t in brain.responsibility]
                traktanden.append(dict(
                    title = conv(brain.Title()),
                    Verantwortlicher = self.get_latex_responsibility(
                        responsibility
                        ),
                    Text = conv(brain.text),
                    Ergebnis = conv(brain.conclusion),
                ))
        latex_traktanden = ['-- %s' % t['title'] for t in traktanden]
        latex_traktanden = '\\newline'.join(latex_traktanden)

        latex.append(r'\begin{longtable}{p{0.3\textwidth}p{0.7\textwidth}}')
        latex.append(r'\multicolumn{2}{l}{\textbf{%s}}\\' % conv(
            context.Title()))
        latex.append(r'\multicolumn{2}{l}{\ }\\')
        latex.append(self.get_row(
            'Termin-Typ',
             self.context.translate(context.getMeeting_type(),
                domain='ftw.meeting')))
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
        latex.append(self.get_row(
            'Verantwortliche',
            self.get_latex_responsibility(self.context.getResponsibility())))
        latex.append(self.get_row('Beschreibung', context.Description()))
        latex.append(self.get_row('Traktanden', latex_traktanden))
        latex.append(r'\end{longtable}')
        latex.append(r'\newline')
        count = 0
        for traktandum in traktanden:
            count += 1
            latex.append(
                r'\begin{longtable}{p{0.3\textwidth}p{0.7\textwidth}}')
            latex.append(r'\multicolumn{2}{l}{\ }\\')
            latex.append(
                r'\multicolumn{2}{l}{\textbf{%s. %s}}\\' % (
                    count, traktandum['title']))
            del traktandum['title']
            for t_key in traktandum.keys():
                latex.append(self.get_row(
                    t_key,
                    traktandum[t_key]))
            latex.append(r'\end{longtable}')
        return '\n'.join(latex)

    def get_row(self, title, value):
        value = value.replace('\\\\', '\\newline\n')
        return r'\textbf{%s} & %s\\' % (title, value)

    def get_latex_responsibility(self, responsibility):
        result = []
        for term in responsibility:
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
            result.append('-- %s' % self.controller.convert(fullname))
        return '\\newline '.join(result)
