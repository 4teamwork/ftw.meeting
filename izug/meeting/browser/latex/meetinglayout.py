class MeetingLayout(object):
    
    def __call__(self, view, context):
        self.view = view
        self.context = context
        self.setDocumentClass()
        self.registerPackages()
        self.appendHeadCommands()
        self.appendAboveBodyCommands()
        self.appendBeneathBodyCommands()

    def getResourceFileData(self, filename, resource='izug.meeting.latex.resource'):
        fiveFile = self.context.restrictedTraverse('++resource++%s/%s' % (resource, filename))
        path = fiveFile.context.path
        fileData = open(path).read()
        return fileData

    def setDocumentClass(self):
        self.view.setLatexProperty('document_class', 'article')
        self.view.setLatexProperty('document_config', 'a4paper,10pt,parskip=half')
        # register logo image
        image = self.getResourceFileData('logo_sw.pdf',
                resource='izug.bibliothek.latex.resource')
        self.view.addImage(uid='logo_sw', image=image)

    def registerPackages(self):
        self.view.registerPackage('graphicx')
        self.view.registerPackage('helvet')
        self.view.registerPackage('wrapfig')
        self.view.registerPackage('longtable')
        self.view.registerPackage('titlesec', 'compact')
        self.view.registerPackage('geometry', 'left=35mm,right=10mm,top=55mm,bottom=30.5mm')
        self.view.registerPackage('fancyhdr')
        self.view.registerPackage('paralist', 'neveradjust')
        self.view.registerPackage('textpos', 'absolute, overlay')
        self.view.registerPackage('ifthen')

    def appendHeadCommands(self):
        self.view.appendHeaderCommand(r'\newcommand{\Autor}{%s}' % r'')
        self.view.appendHeaderCommand(r'\newcommand{\Titel}{%s}' % self.context.pretty_title_or_id())
        self.view.appendHeaderCommand(r'\newcommand{\Adresse}{%s}' % r'')
        head_commands = self.getResourceFileData('head_commands.tex')
        self.view.appendHeaderCommand(head_commands)
        # embed izug.bibliothek head commands
        head_commands = self.getResourceFileData('head_commands.tex',
                resource='izug.bibliothek.latex.resource')
        self.view.appendHeaderCommand(head_commands)

    def appendAboveBodyCommands(self):
        self.view.appendToProperty('latex_above_body', r'\thispagestyle{myheadings}')

    def appendBeneathBodyCommands(self):
        pass
        #self.view.appendToProperty('latex_beneath_body', r'')
        
