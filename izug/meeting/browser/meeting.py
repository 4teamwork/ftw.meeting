from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName

from Products.Five.browser import BrowserView
from plonegov.pdflatex.browser.converter import LatexCTConverter

from plone.memoize import ram

def _get_contents_key(method, self):
    return [b.modified for b in self.context.getFolderContents()]

class MeetingView(BrowserView):

    @ram.cache(_get_contents_key)
    def getFiles(self):
        context = self.context.aq_inner
        query = dict(
                     portal_type = ['File',],
                     sort_on = 'effective',
                     sort_order = 'descending',
        )
        raw = context.getFolderContents(contentFilter=query)
        results = []
        return [dict(title=b.Title,
                     url = b.getURL(),
                     Description=b.Description,
                     Creator=b.Creator,
                     icon = '%s/%s'%(context.portal_url(),b.getIcon)) 
                for b in raw]
                
    
    def renderPoodleTable(self, poodle):
        view = getMultiAdapter((poodle, poodle.REQUEST), name=u'izug_poodle_table')
        return view()
        


class MeetingLatexConverter(LatexCTConverter):
    
    def getDisplayListValue(self, object, fieldname):
        context = object.aq_inner
        field = context.getField(fieldname)
        vocab = field.Vocabulary(context)
        value = field.get(context)
        return context.displayValue(vocab, value)

    def getDisplayListValueFromDataGridField(self, object, fieldname, row, column_id):
        context = object.aq_inner
        field = context.getField(fieldname)
        widget = field.widget
        column_definition = widget.getColumnDefinition(field, column_id)
        vocab = column_definition.getVocabulary(context)
        cell_value = row.get(column_id)
        value = vocab.getValue(cell_value)
        return value and value or cell_value
    
    def __call__(self, context, view):
        self.view = view
        latex = []
        w = lambda *lines:[latex.append(line) for line in lines]
        plone_view = getMultiAdapter((self.context, self.request), name=u'plone')
        latex_date = self.view.convert(plone_view.toLocalizedTime(context.start_date, long_format=False))
        try:
            latex_time = self.view.convert(context.start_date.strftime('%H:%M'))
        except:
            latex_time = self.view.convert('HH:ii')
        latex_title = self.view.convert(context.pretty_title_or_id())
        #w(r'T direkt 041 XXX\\')
        #w(r'E-Mail Adresse\\')
        w(r'Zug, \today\\')
        w()
        w(r'\vspace{3\baselineskip}')
        w(r'{\bf Protokoll} \\')
        w(r'{\bf %s} \\' % latex_title)
        w(r'\vspace{\baselineskip}')
        w(r'Datum: %s \\' % latex_date)
        w(r'Zeit: %s \\' % latex_time)
        w(r'Ort: %s \\' % self.view.convert(context.location))
        w(r'Sitzungsleitung: %s \\' % self.view.convert(self.getDisplayListValue(context, 'head_of_meeting')))
        w(r'%s \\' % self.view.convert('Protokollf&uuml;hrung: %s' % self.getDisplayListValue(context, 'recording_secretary')))
        w()
        w(r'\vspace{\baselineskip}')
        w(r'{\bf Teilnehmende} \\')
        # attendees
        w(r'\begin{attendeeList}')
        for row in self.context.attendees:
            w(r'%s\\' % (
                self.view.convert(self.getDisplayListValueFromDataGridField(context, 'attendees', row, 'contact')),
            ))
        w()
        w(r'\vspace{\baselineskip}')
        w(r'{\bf Traktanden}\\')
        w(r'\vspace{0.5cm}')
        w()
        latex = '\n'.join(latex)
        latex += self.convertChilds(context, self.view)
        return latex
