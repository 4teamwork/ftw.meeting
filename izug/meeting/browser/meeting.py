from zope.component import getMultiAdapter

from plonegov.pdflatex.browser.converter import LatexCTConverter

class MeetingLatexConverter(LatexCTConverter):
    
    def __call__(self, context, view):
        self.view = view
        latex = []
        w = lambda line:latex.append(line)
        plone_view = getMultiAdapter((self.context, self.request), name=u'plone')
        latex_date = self.view.convert(plone_view.toLocalizedTime(context.start_date, long_format=False))
        latex_time = self.view.convert(context.start_date.strftime('%H:%M'))
        latex_title = self.view.convert(context.pretty_title_or_id())
        w(r'{\bf Protokoll} \\')
        w(r'{\bf %s} \\' % latex_title)
        w(r'\vspace{\baselineskip}')
        w(r'Datum: %s \\' % latex_date)
        w(r'Zeit: %s \\' % latex_time)
        w(r'Ort: %s \\' % self.view.convert(context.location))
        w(r'Sitzungsleitung: %s \\' % self.view.convert(context.head_of_meeting))
        w(r'%s \\' % self.view.convert('Protokollf&uuml;hrung: %s' % context.recording_secretary))
        w(r'\vspace{\baselineskip}')
        w(r'{\bf Teilnehmende} \\')
        # attendees
        w(r'\begin{attendeeList}')
        for row in self.context.attendees:
            w('\t\\attendee{%s}{%s}{%s}' % (
                row['contact'],
                (row['present'] and 'X' or ''),
                (row['excused'] and 'X' or ''),
            ))
        w(r'\end{attendeeList}')
        latex = '\n'.join(latex)
        latex += self.convertChilds(context, self.view)
        return latex
