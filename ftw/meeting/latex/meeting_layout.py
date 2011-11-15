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
        self.view.setLatexProperty('document_config',
            'a4paper,10pt,german, oneside')

    def registerPackages(self):
        self.view.registerPackage('inputenc', 'utf8')
        self.view.registerPackage('fontenc', 'T1')
        self.view.registerPackage('babel', 'ngerman')
        self.view.registerPackage('geometry',
            'left=25mm,right=45mm,top=23mm,bottom=30mm')
        self.view.registerPackage('xcolor')
        self.view.registerPackage('graphicx')
        self.view.registerPackage('textcomp')
        self.view.registerPackage('helvet')
        self.view.registerPackage('hyperref',
            'colorlinks=false,breaklinks=true,linkcolor=black,pdfborder={0 0 0}')
        self.view.registerPackage('longtable')

    def appendHeadCommands(self):
        self.view.appendHeaderCommand(
            r'\renewcommand{\familydefault}{\sfdefault}')
        self.view.appendHeaderCommand("\\title{%s}"%(self.context.Title()))

    def appendAboveBodyCommands(self):
        pass

    def appendBeneathBodyCommands(self):
        pass
