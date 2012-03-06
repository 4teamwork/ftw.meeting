from ftw.meeting.interfaces import IMeeting
from ftw.pdfgenerator.interfaces import IBuilder
from ftw.pdfgenerator.layout.makolayout import MakoLayoutBase
from zope.component import adapts
from zope.interface import Interface


class MeetingLayout(MakoLayoutBase):
    adapts(IMeeting, Interface, IBuilder)

    template_directories = ['templates']
    template_name = 'layout.tex'

    def before_render_hook(self):
        self.use_babel()
        self.use_package('inputenc', options='utf8', append_options=False)
        self.use_package('fontenc', options='T1', append_options=False)
        self.use_package('ae,aecompl')
        self.use_package(
            'geometry', options='left=35mm,right=20mm,top=20mm,bottom=25mm',
            append_options=False)
        self.use_package(
            'hyperref', options='colorlinks=false,breaklinks=true,' + \
                'linkcolor=black,pdfborder={0 0 0}', append_options=False)

        self.use_package('helvet')
        self.use_package('titlesec', 'compact')
        self.use_package('fancyhdr')
        self.use_package('enumitem')
        self.use_package('lastpage')
        self.use_package('scrtime')
