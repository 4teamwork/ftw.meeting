from plonegov.pdflatex.browser.converter import LatexCTConverter
from izug.utils.users import getResponsibilityInfosFor


class MeetingAsLaTeX(LatexCTConverter):
    """ LaTeX representation of content type Meeting
    """

    def __call__(self, context, view):
        self.controller = view
        return self.getLaTeXBody()

    def getLaTeXBody(self):
        # shortcut for converting html to latex
        conv = self.controller.convert
        # define a method for easy writing
        latex = []

        def write(*lines):
            latex.extend(lines)
        # add a information comment which indicates
        # that the code is from this view
        seperator = '%% %s' % ('-' * 65)
        write(seperator, r'% MEETING CONTENT',
              '%% PATH: %s' % '/'.join(self.context.getPhysicalPath()),
              seperator, '')
        # add headings.. we use \bf, its easyier
        # XXX: to be replaced (see #904):
        meeting_type = self.context.getMeeting_form().strip()
        meeting_type = meeting_type and meeting_type or 'Protokoll'
        write(r'{\bf %s}\\' % meeting_type)
        write(r'{\bf \Titel}\\')
        write(r'\vspace{\baselineskip}', '')
        # add some informations (dates, times, locations)
        write(*self._get_dates_latex())
        write(r'Ort: %s\\' % conv(self.context.location))
        write(r'Sitzungsleitung: %s\\' % conv(
                self._get_display_list_value(self.context, 'head_of_meeting')))
        write(r'%s\\' % conv('Protokollf&uuml;hrung: %s'
                             % self._get_display_list_value(self.context,
                                                            'recording_secretary')))
        write(r'\vspace{\baselineskip}', '')
        # teilnehmende
        write(r'{\bf Teilnehmende} \\')
        for row in self.context.attendees:
            present = conv({'present':'anwesend',
                        'absent':'abwesend',
                        'excused':'entschuldigt'}.get(row.get('present',''), ''))
            present = len(present) and (", %s" % present) or present 
            write(r'%s%s\\' %
                  (conv(self._get_display_list_value_from_dataGridField(
                        self.context, 'attendees', row, 'contact')),
                        present
                        )
                        )
        write(r'{\vspace{\baselineskip}}', '')
        # traktanden
        write(r'{\bf Traktanden}', r'\vspace{-\baselineskip}')
        write(r'\begin{enumerate}')
        for brain in self._get_children(self.context):
            write(r'\item %s' % conv(brain.Title))
        write(r'\end{enumerate}', '')
        write(r'% define meeting item counter')
        write(r'\newcounter{meetingitem}', '', '')
        write(self.convertChilds(self.context, self.controller))


        related_tasks = [r for r in self.context.relatedItems()
                         if r.portal_type=='Task']
        for obj in self.context.getFolderContents(full_objects=True):
            if obj.portal_type=='Meeting Item':
                for rel in obj.relatedItems():
                    if rel.portal_type=='Task':
                        related_tasks.append(rel)
        if len(related_tasks) > 0:
            table = '<table class="table_border">'
            table += '<colgroup>'
            table += '<col width="1%" />'
            table += '<col width="42%" />'
            table += '<col width="1%" />'
            table += '<col width="25%" />'
            table += '<col width="1%" />'
            table += '<col width="12%" />'
            table += '<col width="1%" />'
            table += '<col width="17%" />'
            table += '</colgroup>'
            table += '<thead>'
            table += '<tr>'
            table += '<td class="underline left">&nbsp;</td>'
            table += '<td class="underline rahmen_r left">Beschluss / Auftrag</td>'
            table += '<td class="underline left">&nbsp;</td>'
            table += '<td class="underline rahmen_r left">Wer</td>'
            table += '<td class="underline left">&nbsp;</td>'
            table += '<td class="underline rahmen_r left">Termin</td>'
            table += '<td class="underline left">&nbsp;</td>'
            table += '<td class="underline rahmen_r left">Status</td>'
            table += '</tr>'
            table += '</thead>'
            table += '<tbody>'
            for task in related_tasks:
                res = [getResponsibilityInfosFor(self.context, responsibility)
                       for responsibility in task.getResponsibility()]
                res = [a['name'] for a in res]
                state = self.context.portal_catalog({'UID': task.UID()})[0].review_state
                table += '<tr><td class="underline">&nbsp;</td>'
                table += '<td class="underline rahmen_r"><b>%s</b><p>&nbsp;</p>%s</td>'\
                         % (task.Title(), task.text)
                table += '<td class="underline">&nbsp;</td>'
                table += '<td class="underline rahmen_r">%s</td>' % '<p>&nbsp;</p>'.join(res)
                table += '<td class="underline">&nbsp;</td>'
                table += '<td class="underline rahmen_r">%s</td>'\
                          % str(self.context.toLocalizedTime(task.end()))
                table += '<td class="underline">&nbsp;</td>'
                table += '<td class="underline rahmen_r">%s</td></tr>' % str(self.context.translate(state))

            table += '</tbody>'
            table += '</table>'
            table = conv(table).strip()

            write(r'\clearpage')
            write(r'\textbf{Pendenzenliste}')
            write(table)
        return '\n'.join(latex)

    def _get_dates_latex(self):
        conv = self.controller.convert
        # define a method for easy writing
        latex = []

        def write(*lines):
            latex.extend(lines)
        if self.context.start_date and self.context.end_date:
            # start and end existing
            start_day = self.context.start_date.strftime('%d.%m.%Y')
            start_time = self.context.start_date.strftime('%H.%M')
            end_day = self.context.end_date.strftime('%d.%m.%Y')
            end_time = self.context.end_date.strftime('%H.%M')
            if start_day==end_day:
                # same date
                write(r'Datum: %s\\' % \
                          conv(start_day))
                write(r'Dauer: %s\,--\,%s\\' % (
                        conv(start_time),
                        conv(end_time)))
            else:
                # different date
                write(r'Start: %s, %s\\' % (
                        conv(start_day),
                        conv(start_time)))
                write(r'Ende: %s, %s\\' % (
                        conv(end_day),
                        conv(end_time)))
        return latex

    def _get_display_list_value(self, object, fieldname):
        context = object.aq_inner
        field = context.getField(fieldname)
        vocab = field.Vocabulary(context)
        value = field.get(context)
        return context.displayValue(vocab, value)

    def _get_display_list_value_from_dataGridField(self, object, fieldname, row, column_id):
        context = object.aq_inner
        field = context.getField(fieldname)
        widget = field.widget
        column_definition = widget.getColumnDefinition(field, column_id)
        vocab = column_definition.getVocabulary(context)
        cell_value = row.get(column_id)
        value = vocab.getValue(cell_value)
        return value and value or cell_value

    def _get_children(self, context=None):
        """ Returns a list of brains, which are children of the
        given or the current context. The list is sorted by
        position in parent.
        """
        context = context or self.context
        query = {
            'path': {
                'query': '/'.join(context.getPhysicalPath()),
                'depth': 1,
                },
            'sort_on': 'getObjPositionInParent',
            }
        return context.portal_catalog(query)


class MeetingItemAsLaTeX(LatexCTConverter):
    """ LaTeX representation of content type Meeting Item
    """

    def __call__(self, context, view):
        self.controller = view
        return self.getLaTeXBody()

    def getLaTeXBody(self):
        # shortcut for converting html to latex
        conv = self.controller.convert
        # define a method for easy writing
        latex = []

        def write(*lines):
            latex.extend(lines)
        # add a information comment which indicates
        # that the code is from this view
        seperator = '%% %s' % ('-' * 65)
        write(seperator, r'% MEETING ITEM CONTENT',
              '%% PATH: %s' % '/'.join(self.context.getPhysicalPath()),
              seperator, '')
        # increase meeting item counter
        write(r'\addtocounter{meetingitem}{1}')
        # heading
        write(r'{\bf \arabic{meetingitem}. %s}\\' %
              conv(self.context.Title()))
        write(conv(self.context.getText()), '')
        if self.context.getConclusion():
            write(r'{\bf Ergebnis:}\\')
            write(conv(self.context.getConclusion()), '')
        responsible = self._get_display_list_value(self.context,
                                                   'responsibility')
        if responsible.strip():
            write(r'{\bf Verantwortlich:}\\')
            write(responsible)
        write('', '')

        return '\n'.join(latex)

    def _get_display_list_value(self, object, fieldname):
        context = object.aq_inner
        field = context.getField(fieldname)
        vocab = field.Vocabulary(context)
        value = field.get(context)
        return context.displayValue(vocab, value)
