from AccessControl import ClassSecurityInfo
from DateTime import DateTime
from DateTime.interfaces import DateTimeError
from Products.ATContentTypes import ATCTMessageFactory as atct_mf
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.lib.calendarsupport import CalendarSupportMixin
from Products.ATReferenceBrowserWidget import ATReferenceBrowserWidget
from Products.Archetypes import atapi
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from Products.DataGridField import DataGridField
from Products.DataGridField.SelectColumn import SelectColumn
from ftw.calendarwidget.browser.widgets import FtwCalendarWidget
from ftw.meeting import meetingMessageFactory as _
from ftw.meeting.config import PROJECTNAME
from ftw.meeting.content.widget import DataGridWidgetExtended
from ftw.meeting.interfaces import IMeeting
from zope import component, schema
from zope.interface import implements


MeetingSchema = folder.ATFolderSchema.copy() + atapi.Schema((
        atapi.DateTimeField(
            name='start_date',
            searchable=True,
            required=True,
            accessor='start',
            schemata='default',
            widget=FtwCalendarWidget(
                helper_js=('start_end_date_helper.js',),
                label=_(u"meeting_label_start_date",
                        default=u"Start Date"),
                description=_(u"meeting_help_start_date",
                              default=u"Enter the starting date and time, "
                                  "or click the calendar icon and select it.")
                )),

        atapi.DateTimeField(
            name='end_date',
            searchable=True,
            required=True,
            accessor='end',
            schemata='default',

            widget=FtwCalendarWidget(
                label=_(
                    u"meeting_label_end_date",
                    default=u"End Date"),
                description=_(
                    u"meeting_help_end_date",
                    default=u"Enter the ending date and time, "
                    "or click the calendar icon and select it."))),

        atapi.StringField(
            name='meeting_type',
            searchable=False,
            schemata='default',
            required=True,
            default='event',
            vocabulary_factory='ftw.meeting.types',

            widget=atapi.SelectionWidget(
                label=_(u"meeting_label_type", default=u"Event type"),
                description=_(u"meeting_help_type",
                              default=u"Choose your event type."),
                helper_js=['meeting_toggle_date.js', ],
                format='radio')),

        DataGridField(
            name='responsibility',
            searchable=False,
            schemata='default',
            columns=('contact', ),
            allow_empty_rows=False,

            widget=DataGridWidgetExtended(
                label=_(u"meeting_label_responsibility",
                        default=u"Responsibility"),
                description=_(
                    u"meeting_help_responsibility",
                    default=u"Enter the responsible of the meeting."),
                auto_insert=True,
                select_all_column='contact',
                columns={
                    'contact':
                        SelectColumn(
                        label=_(
                            u"meeting_label_responsibility",
                            default="Responsibility"),
                        vocabulary='getAttendeesVocabulary'
                        ),
                    })),

        atapi.StringField(
            name='meeting_form',
            required=False,
            searchable=True,
            schemata='meeting',
            vocabulary='getMeetingForms',

            widget=atapi.SelectionWidget(
                label=_(u"meeting_label_meeting_form",
                        default=u"Meeting Form"),
                description=_(u"meeting_help_meeting_form",
                              default=u"Choose your Meeting form."),
                format='radio')),

        atapi.LinesField(
            name='head_of_meeting',
            required=False,
            searchable=True,
            schemata='meeting',
            index='KeywordIndex:schema',
            vocabulary_factory='ftw.meeting.users',

            widget=atapi.SelectionWidget(
                label=_(u"meeting_label_head_of_meeting",
                        default=u"Head of Meeting"),
                description=_(u"meeting_help_head_of_meeting",
                              default=u"Select the head of the meeting."))),

        atapi.LinesField(
            name='recording_secretary',
            required=False,
            searchable=True,
            schemata='meeting',
            index='KeywordIndex:schema',
            vocabulary_factory='ftw.meeting.users',

            widget=atapi.SelectionWidget(
                label=_(u"meeting_label_recording_secretary",
                        default=u"Recording Secretary"),
                description=_(u"meeting_help_recording_secretary",
                              default=u"Select the recording secretary."))),

        DataGridField(
            name='attendees',
            searchable=True,
            schemata='meeting',
            columns=('contact', 'present'),
            allow_empty_rows=False,

            widget=DataGridWidgetExtended(
                label=_(u"meeting_label_attendees",
                        default=u"Attendees"),
                description=_(u"meeting_help_attendees",
                              default=u"Enter the attendees of the meeting."),
                auto_insert=True,
                select_all_column='contact',

                columns={
                    'contact': SelectColumn(
                        label=_(
                            u"meeting_label_attendees_attendee",
                            default=u"Attendee"),
                        vocabulary='getAttendeesVocabulary'
                        ),
                    'present': SelectColumn(
                        label=_(
                            u"meeting_label_attendees_present",
                            default=u"Present"),
                        vocabulary='getPresentOptions',
                        ),
                    })),

        atapi.ReferenceField(
            name='related_items',
            relationship='relatesTo',
            multiValued=True,
            isMetadata=True,
            schemata='default',
            languageIndependent=False,

            widget=ATReferenceBrowserWidget.ReferenceBrowserWidget(
                allow_search=True,
                allow_browse=True,
                show_indexes=False,
                force_close_on_insert=False,
                label=_(u"meeting_label_related_items",
                        default=u"Related Items"),
                description=_(u"meeting_help_related_items",
                              default=u""),
                visible={'edit': 'visible', 'view': 'invisible'}
                )),
        atapi.ReferenceField(
            name='pdf_representation',
            relationship='pdfRepresentation',
            multiValued=False,
            schemata='default',
            languageIndependent=False,
            widget=ATReferenceBrowserWidget.ReferenceBrowserWidget(
                visible={'edit': 'invisible', 'view': 'invisible'}
            )),
    ))


MeetingSchema.changeSchemataForField('effectiveDate', 'settings')
MeetingSchema.changeSchemataForField('expirationDate', 'settings')


# use plone default location field
MeetingSchema.moveField('location', after='end_date')
MeetingSchema.moveField('description', after='end_date')
MeetingSchema['location'].searchable = True
MeetingSchema['location'].schemata = 'default'
MeetingSchema['location'].widget = atapi.StringWidget(
    label=_(u"meeting_label_location", default=u"Location"),
    description=_(
        u"meeting_help_location",
        default=u"Enter the location where the meeting will take place."),
    )
MeetingSchema['location'].write_permission = permissions.ModifyPortalContent

MeetingSchema.changeSchemataForField('effectiveDate', 'settings')
MeetingSchema.changeSchemataForField('expirationDate', 'settings')
MeetingSchema['effectiveDate'].widget.visible = {'view': 'invisible',
                                                 'edit': 'invisible'}
MeetingSchema['expirationDate'].widget.visible = {'view': 'invisible',
                                                  'edit': 'invisible'}


class Meeting(folder.ATFolder, CalendarSupportMixin):
    """A type for meetings."""
    implements(IMeeting)
    security = ClassSecurityInfo()

    portal_type = "Meeting"
    schema = MeetingSchema

    # based on Products.ATContentTypes.content.event.ATEvent
    security.declareProtected(permissions.View, 'post_validate')
    def post_validate(self, REQUEST=None, errors=None):
        """Validates start and end date

        End date must be after start date
        """
        if 'start_date' in errors or 'end_date' in errors:
            # No point in validating bad input
            return

        rstartDate = REQUEST.get('start_date', None)
        rendDate = REQUEST.get('end_date', None)

        if rendDate:
            try:
                end = DateTime(rendDate)
            except DateTimeError:
                errors['end_date'] = atct_mf(u'error_invalid_end_date',
                                      default=u'End date is not valid.')
        else:
            end = self.end()
        if rstartDate:
            try:
                start = DateTime(rstartDate)
            except DateTimeError:
                errors['start_date'] = _(u'error_invalid_start_date',
                                        default=u'Start date is not valid.')
        else:
            start = self.start()

        if 'start_date' in errors or 'end_date' in errors:
            # No point in validating bad input
            return

        if start > end:
            errors['end_date'] = atct_mf(
                u'error_end_must_be_after_start_date',
                default=u'End date must be after start date.')

    def getAttendeesVocabulary(self):
        """Workaround for DatagridField SelectColumn
        Because SelectColumn doesn't suppoert vocabulary_factory

        """
        factory = component.getUtility(
            schema.interfaces.IVocabularyFactory,
            name='ftw.meeting.users',
            context=self)

        # converts the list of simpleterms into a displaylist
        # and resturns the result directly
        display_list = atapi.DisplayList()
        for term in factory(self):
            display_list.add(term.value, term.title or term.token)
        return display_list

    def getResponsibilityInfos(self, userids):
        """calls an utility, which returns a list of users
        format: {'fullname':'Demo User', 'url':'portal/author/userid'}

        """
        result = []
        if not userids:
            return
        elif isinstance(userids, list) or isinstance(userids, tuple):
            for userid in userids:
                result.append(self.getUserInfos(userid))
        else:
            result.append(self.getUserInfos(userids))
        return result

    @property
    def endDate(self):
        return self.end_date

    @property
    def startDate(self):
        return self.start_date

    def setStartDate(self, date):
        self.getField('start_date').set(self, date)

    def setEndDate(self, date):
        self.getField('end_date').set(self, date)

    def getUserInfos(self, userid):
        """ return a dict with userinformations, about the user """
        mt = getToolByName(self, 'portal_membership')
        user = mt.getMemberById(userid)

        if user:
            fullname = user.getProperty('fullname', '')
            if not fullname:
                fullname = userid
            return {'name': fullname,
                    'url': '%s/author/%s' % (
                    self.portal_url(),
                    user.id,
                    )}
        else:
            catalog = getToolByName(self, 'portal_catalog')
            brains = catalog(dict(UID=userid))
            if len(brains):
                brain = brains[0]
                return {'name': brain.Title, 'url': brain.getPath()}
            return {'name': userid, 'url': ''}

    def getPresentOptions(self):
        """returns present options

        """
        return atapi.DisplayList(
            (
                ('present', _(u'present')),
                ('absent', _(u'absent')),
                ('excused', _(u'excused'))))

    def getAttendeesOrUsers(self):

        def _get_usernames(data):
            names = []
            for item in data:
                if item and isinstance(item, (str, unicode)):
                    names.append(item)

                elif isinstance(item, dict):
                    name = item.get('contact', None)
                    if name:
                        names.append(name)

            return names

        usernames = _get_usernames(self.getResponsibility())

        if self.getMeeting_type() == 'meeting':
            usernames += _get_usernames(self.getHead_of_meeting())
            usernames += _get_usernames(self.getRecording_secretary())
            usernames += _get_usernames(self.getAttendees())

        usernames = list(set(usernames))

        return usernames

    def getMeetingTypes(self):
        """Returns a DisplayList of meeting types
        The ids are schemata names concatenated by _


        """
        return atapi.DisplayList((
                ('dates_additional', _(u'meeting_type_event')),
                ('meeting_dates_additional', _(u'meeting_type_meeting'))))

    def getMeetingForms(self):
        """Returns a DisplayList of meeting forms from property

        """
        values = atapi.DisplayList()
        m_props = self.portal_properties.get('ftw_meeting_properties')
        if m_props:
            for item in getattr(m_props, 'meeting_form'):
                values.add(item, item)
        return values.sortedByValue()

    #information for ical export
    def getEventType(self):
        return False

    def contact_name(self):
        return ','.join(self.getHead_of_meeting())

    def contact_phone(self):
        return ""

    def contact_email(self):
        return ""

    def event_url(self):
        return self.absolute_url()

    @property
    def sortAttribute(self):
        return 'getObjPositionInParent'

    @property
    def sortOrder(self):
        return 'ascending'

    def sortable_responsibility(self):
        if self.getResponsibility():
            return [r['contact'] for r in self.getResponsibility()]

    security.declarePublic('canSetDefaultPage')
    def canSetDefaultPage(self):
        return False


atapi.registerType(Meeting, PROJECTNAME)
