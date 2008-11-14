class MeetingLayout(object):
    
    def __call__(self, view, context):
        self.view = view
        self.context = context
        self.setDocumentClass()
        self.registerPackages()
        self.appendHeadCommands()
        self.appendAboveBodyCommands()
        self.appendBeneathBodyCommands()

    def getResourceFileData(self, filename):
        fiveFile = self.context.restrictedTraverse('++resource++izug.meeting.latex.resource/%s' % filename)
        path = fiveFile.context.path
        fileData = open(path).read()
        return fileData

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
        self.view.registerPackage('scrpage2', 'automark')
        self.view.registerPackage('titlesec', 'compact')
        self.view.registerPackage('geometry', 'left=1.7cm,top=2.5cm,right=7.5cm')

    def appendHeadCommands(self):
        head_commands = self.getResourceFileData('head_commands.tex')
        self.view.appendHeaderCommand(head_commands)

    def appendAboveBodyCommands(self):
        pass
        #self.view.appendToProperty('latex_above_body', r'')

    def appendBeneathBodyCommands(self):
        pass
        #self.view.appendToProperty('latex_beneath_body', r'')
        
