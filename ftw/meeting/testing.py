from plone.testing import Layer
from plone.testing import zca
from zope.configuration import xmlconfig


class LatexZCMLLayer(Layer):
    """A layer which only sets up the zcml, but does not start a zope
    instance.
    """

    defaultBases = (zca.ZCML_DIRECTIVES,)

    def testSetUp(self):
        self['configurationContext'] = zca.stackConfigurationContext(
            self.get('configurationContext'))

        import ftw.meeting.latex
        xmlconfig.file('configure.zcml', ftw.meeting.latex,
                       context=self['configurationContext'])

    def testTearDown(self):
        del self['configurationContext']


LATEX_ZCML_LAYER = LatexZCMLLayer()
