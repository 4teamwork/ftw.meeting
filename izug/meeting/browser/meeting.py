from zope.component import getMultiAdapter

from plonegov.pdflatex.browser.converter import LatexCTConverter

class MeetingLatexConverter(LatexCTConverter):
    
    def __call__(self, context, view):
        self.view = view
        plone_view = getMultiAdapter((self.context, self.request), name=u'plone')
        latexDate = self.view.convert(plone_view.toLocalizedTime(context.start_date, long_format=False))
        latex = ''
        latex_title = self.view.convert(context.pretty_title_or_id())
        latex += r'{\Huge \bf %s} \\' % latex_title
        latex += '\n'
        latex += r'\vspace{1.5cm}'
        latex += '\n'
        latex += r'\begin{footnotesize}'
        latex += '\n'
        latex += r'\begin{tabular}{p{4cm}|l}'
        latex += '\n'
        latex += r'\rule[4mm]{14cm}{0.5pt} \\'
        latex += '\n'
        latex += r'%s & %s \\' % ('Beschreibung:', self.view.convert(context.description))
        latex += '\n'
        latex += r'%s & %s \\' % ('Ort:', self.view.convert(context.location))
        latex += '\n'
        latex += r'%s & %s \\' % ('Sitzungsleitung:', self.view.convert(context.head_of_meeting))
        latex += '\n'
        latex += r'%s & %s \\' % ('Protokollfuehrung:', self.view.convert(context.recording_secretary))
        latex += '\n'
        latex += r'\end{tabular}'
        latex += '\n'
        latex += r'\end{footnotesize}'
        latex += '\n'
        latex += '\n'
        latex += r'\begin{attendeeList}' + '\n'
        for row in self.context.attendees:
            latex += '\t\\attendee{%s}{%s}{%s}\n' % (
                row['contact'],
                (row['present'] and 'X' or ''),
                (row['excused'] and 'X' or ''),
            )
        latex += r'\end{attendeeList}' + '\n'
        latex += self.convertChilds(context, self.view)
        return latex
