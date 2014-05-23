from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from plone.app.testing import applyProfile
from plone.app.testing import IntegrationTesting, FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import Layer
from plone.testing import z2
from plone.testing import zca
from zope.configuration import xmlconfig
import ftw.meeting.tests.builders


class LatexZCMLLayer(Layer):
    """A layer which only sets up the zcml, but does not start a zope
    instance.
    """

    defaultBases = (zca.ZCML_DIRECTIVES,)

    def testSetUp(self):
        self['configurationContext'] = zca.stackConfigurationContext(
            self.get('configurationContext'))

        import zope.traversing
        xmlconfig.file('configure.zcml', zope.traversing,
                       context=self['configurationContext'])

        import ftw.pdfgenerator.tests
        xmlconfig.file('test.zcml', ftw.pdfgenerator.tests,
                       context=self['configurationContext'])

        import ftw.pdfgenerator
        xmlconfig.file('configure.zcml', ftw.pdfgenerator,
                       context=self['configurationContext'])

        import ftw.meeting.latex
        xmlconfig.file('configure.zcml', ftw.meeting.latex,
                       context=self['configurationContext'])

    def testTearDown(self):
        del self['configurationContext']


class FtwMeetingLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import ftw.poodle
        xmlconfig.file('configure.zcml',
                       ftw.poodle,
                       context=configurationContext)
        z2.installProduct(app, 'ftw.poodle')

        import ftw.meeting
        xmlconfig.file('configure.zcml',
                       ftw.meeting,
                       context=configurationContext)

        import ftw.task
        xmlconfig.file('configure.zcml',
                       ftw.task,
                       context=configurationContext)

        import ftw.zipexport
        xmlconfig.file('configure.zcml',
                       ftw.zipexport,
                       context=configurationContext)

        import Products.DataGridField
        xmlconfig.file('configure.zcml',
                       Products.DataGridField,
                       context=configurationContext)

        # installProduct() is *only* necessary for packages outside
        # the Products.* namespace which are also declared as Zope 2 products,
        # using <five:registerPackage /> in ZCML.
        z2.installProduct(app, 'ftw.meeting')
        z2.installProduct(app, 'Products.DataGridField')
        z2.installProduct(app, 'ftw.task')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'ftw.poodle:default')
        applyProfile(portal, 'Products.DataGridField:default')
        applyProfile(portal, 'ftw.meeting:file')
        applyProfile(portal, 'ftw.task:default')


FTW_MEETING_FIXTURE = FtwMeetingLayer()
FTW_MEETING_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FTW_MEETING_FIXTURE,), name="FtwMeeting:Integration")
FTW_MEETING_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FTW_MEETING_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="FtwMeeting:functional")

LATEX_ZCML_LAYER = LatexZCMLLayer()
