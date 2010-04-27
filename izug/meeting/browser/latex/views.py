from plonegov.pdflatex.browser.converter import LatexCTConverter


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
        write(r'{\bf %s}\\' % self.context.getMeeting_form())
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
            write(r'%s\\' %
                  conv(self._get_display_list_value_from_dataGridField(
                        self.context, 'attendees', row, 'contact')))
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
