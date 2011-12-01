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
        catalog = getToolByName(self.context, 'portal_catalog')
        # define a method for easy writing
        latex = []
        latex.append(r'\renewcommand{\arraystretch}{1.5}')

        # pdf_logo
        portal = getToolByName(context, 'portal_url').getPortalObject()
        img = portal.unrestrictedTraverse('pdf_logo', None)
        if img:
            self.controller.addImage(uid='pdf_logo', image=img)
            latex.append(r'\includegraphics{pdf_logo}')

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
                    relatedItems = brain.getRelatedItems(),
                ))


        latex_traktanden = ['\\item{%s}' % t['title'] for t in traktanden]
        latex_traktanden = '\n'.join(latex_traktanden)

        latex.append(r'\begin{longtable}{p{0.3\textwidth}p{0.7\textwidth}}')
        latex.append(r'\multicolumn{2}{l}{\textbf{%s}}\\' % conv(
            context.Title()))
        latex.append(r'\multicolumn{2}{l}{\ }\\')
        latex.append(self.get_row(
            'Termin-Typ',
             self.context.translate(context.getMeeting_type(),
                domain='ftw.meeting')).encode('utf8'))
        latex.append(self.get_row(
            'Datum',
            context.toLocalizedTime(context.start(), long_format=1)).encode('utf8'))
        if self.context.getLocation():
            latex.append(self.get_row(
                    'Ort',
                    conv(self.context.getLocation())))
        latex.append(self.get_row(
            'Verantwortliche',
            self.get_latex_responsibility(self.context.getResponsibility())))

        if self.context.getAttendees():
            latex.append(self.get_row(
                    'Teilnehmer',
                    self.get_latex_responsibility(self.context.getAttendees())))
        if self.context.getRecording_secretary():
            brains = [{'contact': uuid} for uuid in self.context.getRecording_secretary()]

            latex.append(self.get_row(
                    'Schriftf"uhrer',
                    self.get_latex_responsibility(brains)))
        if self.context.getHead_of_meeting():
            brains = [{'contact':uuid} for uuid in self.context.getHead_of_meeting()]
            latex.append(self.get_row(
                    'Sitzungsleitung',
                    self.get_latex_responsibility(brains)))

        latex.append(self.get_row('Beschreibung', context.Description()))
        if latex_traktanden:
            latex.append(self.get_row('Traktanden', '\\vspace{-2em}\n\\begin{enumerate}[leftmargin=*]%s\\end{enumerate}' % latex_traktanden))
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

            if traktandum['Verantwortlicher']:
                latex.append(self.get_row(
                        'Verantwortlicher',
                        traktandum['Verantwortlicher']))
            if traktandum['Text']:
                latex.append(self.get_row(
                        'Text',
                        traktandum['Text']))
            if traktandum['Ergebnis']:
                latex.append(self.get_row(
                        'Ergebnis',
                        traktandum['Ergebnis']))
            related_items = []
            for rel_item in traktandum['relatedItems']:
                related_items.append(
                    '\\item[--]{%s (%s, %sKB) \\\\ \\href{%s}{%s}}' % (
                        conv(rel_item.Title()),
                        conv(self.context.lookupMime(rel_item.getContentType()).encode('utf8')),
                        rel_item.get_size() / 1024,
                        rel_item.absolute_url(),
                        rel_item.absolute_url()))
            if len(related_items):
                latex.append(self.get_row(
                        'Verwandte Inhalte',
                        '\\vspace{-2em}\n\\begin{itemize}[leftmargin=*]\n%s\n\\end{itemize}' % '\n'.join(related_items)))

            latex.append(r'\end{longtable}')
        # Pendenzenliste
        related_tasks = [r for r in self.context.getRelated_items()
                         if r.portal_type=='Task']
        for obj in self.context.getFolderContents(full_objects=True):
            if obj.portal_type=='Meeting Item':
                for rel in obj.getRelated_items():
                    if rel.portal_type=='Task':
                        related_tasks.append(rel)

        if related_tasks:
            mt = getToolByName(context, 'portal_membership')
            latex.append(r'\textbf{Pendenzenliste}')
            latex.append(r'\begin{longtable}{|p{0.4\textwidth}|p{0.3\textwidth}|p{0.15\textwidth}|p{0.15\textwidth}|}\hline')
            latex.append(r'Beschluss / Auftrag & Wer & Termin & Status \\ \hline')
            for task in related_tasks:
                res = []
                for userid in task.getResponsibility():
                    member = mt.getMemberById(userid)
                    if member:
                        res.append(member.getProperty('fullname', userid))
                    else:
                        res.append(userid)
                state = catalog({'UID': task.UID()})[0].review_state
                latex.append(r'{\bf %s} \newline %s & %s & %s & %s \\ \hline' %
                             (conv(task.Title()), conv(task.text),
                              '\\newline '.join(res),
                              conv(self.context.toLocalizedTime(task.end())),
                              conv(str(self.context.translate(state)))))
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
            result.append(self.controller.convert(fullname))
        return '\\newline '.join(result)
