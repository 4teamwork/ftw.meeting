class MeetingLayout(object):
    
    def __call__(self, view, context):
        self.view = view
        self.context = context
        self.setDocumentClass()
        self.registerPackages()
        self.appendHeadCommands()
        self.appendAboveBodyCommands()
        self.appendBeneathBodyCommands()

    def setDocumentClass(self):
        self.view.setLatexProperty('document_class', 'scrartcl')
        self.view.setLatexProperty('document_config', 'a4paper,10pt,headsepline,parskip=half')
        self.view.appendHeaderCommand(r'\sloppy')
        self.view.appendHeaderCommand(r'\raggedbottom')

    def registerPackages(self):
        self.view.registerPackage('ucs')
        self.view.registerPackage('graphicx')
        self.view.registerPackage('helvet')
        self.view.registerPackage('wrapfig')
        self.view.registerPackage('longtable')
        self.view.registerPackage('lastpage')

    def appendHeadCommands(self):
        self.view.appendHeaderCommand(r'\setkomafont{section}{\normalsize\sffamily}')
        self.view.appendHeaderCommand(r'\usepackage[automark]{scrpage2}')
        self.view.appendHeaderCommand(r'\renewcommand{\familydefault}{\sfdefault}')        
        self.view.appendHeaderCommand(r'\usepackage[compact]{titlesec}')
        self.view.appendHeaderCommand(r'\titlespacing{\section}{0pt}{-8mm}{*0}')
        self.view.appendHeaderCommand(r'\titlespacing{\subsection}{0pt}{*0}{*0}')
        self.view.appendHeaderCommand(r'\titlespacing{\subsubsection}{0pt}{*0}{*0}\renewcommand\arraystretch{1.5}')
        self.view.appendHeaderCommand(r'\pagestyle{scrheadings}')
        self.view.appendHeaderCommand(r'\setheadwidth[0.7cm]{18.5cm}')
        self.view.appendHeaderCommand(r'\setfootwidth[0.7cm]{18.5cm}')
        self.view.appendHeaderCommand(r'\usepackage[left=1.7cm,top=2.5cm,right=7.5cm]{geometry}')

        checkbox_command = r'\newcommand{\checkbox}[1]{\tiny \setlength{\tabcolsep}{3pt} \begin{tabular}{|p{5pt}|}'
        checkbox_command += '\n'
        checkbox_command += r'\hline'
        checkbox_command += '\n'
        checkbox_command += r'\tiny #1 \\'
        checkbox_command += '\n'
        checkbox_command += r'\hline'
        checkbox_command += '\n'
        checkbox_command += r'\end{tabular}\normalsize}'
        checkbox_command += '\n'
        self.view.appendHeaderCommand(checkbox_command)
        
        meetingitem_command = r'\newcommand{\meetingitem}[2]{'
        meetingitem_command += '\n'
        meetingitem_command += r'\rule[1ex]{18.5cm}{1pt}' 
        meetingitem_command += '\n'
        meetingitem_command += r'{\bf #1}'
        meetingitem_command += '\n'
        meetingitem_command += r'\marginpar{'
        meetingitem_command += '\n'
        meetingitem_command += r'\vspace{-4mm}'
        meetingitem_command += '\n'
        meetingitem_command += r'\begin{tabular}{|p{5cm}}'
        meetingitem_command += '\n'
        meetingitem_command += r'#2 \\'
        meetingitem_command += '\n'
        meetingitem_command += r'\end{tabular}}'
        meetingitem_command += '\n'
        meetingitem_command += r'}'
        meetingitem_command += '\n'
        self.view.appendHeaderCommand(meetingitem_command)

        meetingitemtextblock_command = r'\newcommand{\meetingitemtextblock}[2]{'
        meetingitemtextblock_command += r'{\list{}{'
        meetingitemtextblock_command += r'\setlength{\leftmargin}{0cm}\setlength{\rightmargin}{0cm}}\relax}{\endlist}'
        meetingitemtextblock_command += r'{\bf #1: }'
        meetingitemtextblock_command += r'#2}'
        meetingitemtextblock_command += '\n'
        self.view.appendHeaderCommand(meetingitemtextblock_command)
        
        meetingitemheader_command = r'\newcommand{\meetingitemheader}{'
        meetingitemheader_command += '\n'
        meetingitemheader_command += r'\marginpar{'
        meetingitemheader_command += '\n'
        meetingitemheader_command += r'\vspace{-4mm}'
        meetingitemheader_command += '\n'
        meetingitemheader_command += r'\begin{tabular}{p{5cm}}'
        meetingitemheader_command += '\n'
        meetingitemheader_command += r'Verantwortung \\'
        meetingitemheader_command += '\n'
        meetingitemheader_command += r'\end{tabular}'
        meetingitemheader_command += '\n'
        meetingitemheader_command += r'}'
        meetingitemheader_command += '\n'
        meetingitemheader_command += r'}'
        meetingitemheader_command += '\n'
        self.view.appendHeaderCommand(meetingitemheader_command)

    def appendAboveBodyCommands(self):
        pass
        #self.view.appendToProperty('latex_above_body', r'')

    def appendBeneathBodyCommands(self):
        pass
        #self.view.appendToProperty('latex_beneath_body', r'')
        