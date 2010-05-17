"""Definition of the Meeting content type
"""

from DateTime import DateTime

from izug.arbeitsraum.content.utilities import finalizeIzugSchema
from izug.meeting import meetingMessageFactory as _
from izug.meeting.config import PROJECTNAME
from izug.meeting.interfaces import IMeeting
from izug.poodle.content.poodle import Poodle, PoodleSchema
from izug.poodle.interfaces import IPoodle
from izug.utils.users import getAssignableUsers
from izug.utils.users import getResponsibilityInfosFor

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.lib.calendarsupport import CalendarSupportMixin
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.CMFCore import permissions
from Products.DataGridField import DataGridField
from Products.DataGridField.SelectColumn import SelectColumn

from zope.interface import implements

from widget import DataGridWidgetExtended

MeetingSchema = folder.ATFolderSchema.copy() + atapi.Schema((

     atapi.StringField('meeting_type',
                      searchable = False,
                      schemata = 'default',
                      required = True,
                      default="dates_additional",
                      vocabulary = 'getMeetingTypes',
                      storage = atapi.AnnotationStorage(),
                      widget = atapi.SelectionWidget(label = _(u"meeting_label_type", default=u"Event type"),
                                                     description = _(u"meeting_help_type", default=u"Choose your event type."),
                                                     helper_js = ['meeting_toggle_date.js', ],
                                                     format='radio',
                                                     ),
                      ),
     DataGridField('responsibility',
                   searchable = False,
                   schemata = 'default',
                   columns = ('contact', ),
                   allow_empty_rows = False,
                   storage = atapi.AnnotationStorage(),
                   widget = DataGridWidgetExtended(label = _(u"meeting_label_responsibility", default=u"responsibility"),
                                           description = _(u"meeting_help_responsibility", default=u"Enter the responsible of the meeting."),
                                           auto_insert = True,
                                           select_all_column = 'contact',
                                           columns = {'contact': SelectColumn(title = _(u"meeting_label_responsibility", default="Enter the responsible of the meeting."),
                                                                               vocabulary = 'getAssignableUsers'
                                                                               ),
                                                      }
                                           )
                   ),


    atapi.DateTimeField('start_date',
                        searchable = True,
                        accessor='start',
                        schemata = 'dates',
                        storage = atapi.AnnotationStorage(),
                        widget = atapi.CalendarWidget(label = _(u"meeting_label_start_date", default=u"Start of Meeting"),
                                                      description = _(u"meeting_help_start_date", default=u"Enter the starting date and time, or click the calendar icon and select it."),
                                                      ),
                        ),


    atapi.DateTimeField('end_date',
                        searchable = True,
                        accessor='end',
                        schemata = 'dates',
                        storage = atapi.AnnotationStorage(),
                        widget = atapi.CalendarWidget(label = _(u"meeting_label_end_date", default=u"End of Meeting"),
                                                      description = _(u"meeting_help_end_date", default=u"Enter the ending date and time, or click the calendar icon and select it."),
                                                      ),
                        ),

    atapi.StringField('meeting_form',
                     required = False,
                     searchable = True,
                     schemata = 'meeting',
                     vocabulary = 'getMeetingForms',
                     storage = atapi.AnnotationStorage(),
                     widget = atapi.SelectionWidget(label = _(u"meeting_label_meeting_form", default=u"Meeting Form"),
                                                    description = _(u"meeting_help_meeting_form", default=u"Choose your Meeting form."),
                                                    format='radio',
                                                    ),
                     ),

     atapi.LinesField('head_of_meeting',
                      required = False,
                      searchable = True,
                      schemata = 'meeting',
                      index = 'KeywordIndex:schema',
                      vocabulary = 'getAssignableUsers',
                      storage = atapi.AnnotationStorage(),
                      widget = atapi.SelectionWidget(label = _(u"meeting_label_head_of_meeting", default=u"Head of Meeting"),
                                                     description = _(u"meeting_help_head_of_meeting", default=u"Select the head of the meeting."),
                                                     ),
                      ),

     atapi.LinesField('recording_secretary',
                      required = False,
                      searchable = True,
                      schemata = 'meeting',
                      index = 'KeywordIndex:schema',
                      vocabulary = 'getAssignableUsers',
                      storage = atapi.AnnotationStorage(),
                      widget = atapi.SelectionWidget(label = _(u"meeting_label_recording_secretary", default=u"Recording Secretary"),
                                                     description = _(u"meeting_help_recording_secretary", default=u"Select the recording secretary."),
                                                     ),
                      ),

    DataGridField('attendees',
                  searchable = True,
                  schemata = 'meeting',
                  columns = ('contact',),
                  allow_empty_rows = False,
                  storage = atapi.AnnotationStorage(),
                  widget = DataGridWidgetExtended(label = _(u"meeting_label_attendees", default=u"Attendees"),
                                          description = _(u"meeting_help_attendees", default=u"Enter the attendees of the meeting."),
                                          auto_insert = True,
                                          select_all_column = 'contact',
                                          columns = {'contact': SelectColumn(title = _(u"meeting_label_attendees_attendee", default=u"Attendee"),
                                                                              vocabulary = 'getAssignableUsers'
                                                                              ),
                                                     }
                                          )
                  ),

    atapi.ReferenceField('related_items',
                         relationship = 'relatesTo',
                         multiValued = True,
                         isMetadata = True,
                         schemata = 'additional',
                         languageIndependent = False,
                         index = 'KeywordIndex',
                         accessor = 'relatedItems',
                         allowed_types = ('File', 'Document', 'Meeting', 'Task'),
                         storage = atapi.AnnotationStorage(),
                         widget = ReferenceBrowserWidget(
                                                         allow_search = True,
                                                         allow_browse = True,
                                                         show_indexes = False,
                                                         force_close_on_insert = False,
                                                         label = _(u"meeting_label_related_items", default=u"Related Items"),
                                                         description = _(u"meeting_help_related_items", default=u""),
                                                         visible = {'edit': 'visible', 'view': 'invisible' }
                                                         ),
                         ),

)) + PoodleSchema.copy()

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

MeetingSchema['title'].storage = atapi.AnnotationStorage()
MeetingSchema['description'].storage = atapi.AnnotationStorage()
MeetingSchema['description'].required = True

#Poodle "real" integration
MeetingSchema.changeSchemataForField('users', 'poodle')
MeetingSchema['users'].required = False
MeetingSchema.changeSchemataForField('dates', 'poodle')


finalizeIzugSchema(MeetingSchema, folderish=True, moveDiscussion=False)

MeetingSchema.changeSchemataForField('effectiveDate', 'settings')
MeetingSchema.changeSchemataForField('expirationDate', 'settings')

#we do this after finalizeIzugSchema, oherwise the location field will
#be invisible
#use plone default location field
MeetingSchema.moveField('location', after='description')
MeetingSchema['location'].searchable = True
MeetingSchema['location'].storage = atapi.AnnotationStorage()
MeetingSchema['location'].schemata = 'default'
MeetingSchema['location'].widget = atapi.StringWidget(label = _(u"meeting_label_location", default=u"Location"),
                                                  description = _(u"meeting_help_location", default=u"Enter the location where the meeting will take place."),
                                                  )

MeetingSchema['location'].write_permission = permissions.ModifyPortalContent


#instead of...
"""
    atapi.StringField('location',
                      searchable = True,
                      storage = atapi.AnationStorage(),
                      widget = atapi.StringWidget(label = _(u"meeting_label_location", default=u"Location"),
                                                  description = _(u"meeting_help_location", default=u"Enter the location where the meeting will take place."),
                                                  ),
                      ),
"""


MeetingSchema.changeSchemataForField('effectiveDate', 'settings')
MeetingSchema.changeSchemataForField('expirationDate', 'settings')
MeetingSchema['effectiveDate'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}
MeetingSchema['expirationDate'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}


class Meeting(folder.ATFolder, Poodle, CalendarSupportMixin):
    """A type for meetings."""
    implements(IMeeting, IPoodle)

    portal_type = "Meeting"
    schema = MeetingSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    location = atapi.ATFieldProperty('location')
    no_date = atapi.ATFieldProperty('no_date')
    start_date = atapi.ATFieldProperty('start_date')
    end_date = atapi.ATFieldProperty('end_date')
    head_of_meeting = atapi.ATFieldProperty('head_of_meeting')
    recording_secretary = atapi.ATFieldProperty('recording_secretary')
    responsibility = atapi.ATFieldProperty('responsibility')
    attendees = atapi.ATFieldProperty('attendees')
    related_items = atapi.ATFieldProperty('related_items')

    def at_post_create_script(self):
        #set start and enddate for surveys after creation
        if self.getMeeting_type() == 'poodle_additional':
            self.start_date = DateTime()
            self.end_date = DateTime()+10000
            self.reindexObject()

    def getResponsibilityInfos(self, userids):
        result = []
        if not userids:
            return
        elif isinstance(userids, list) or isinstance(userids, tuple):
            for userid in userids:
                result.append(getResponsibilityInfosFor(self, userid))
        else:
            result.append(getResponsibilityInfosFor(self, userids))
        return result


    def getAssignableUsers(self):
        """Collect users with a given role and return them in a list.
        """
        results = atapi.DisplayList()
        results.add('', _(u'Choose a person'))
        return (results + atapi.DisplayList(getAssignableUsers(self, 'Reader')))

    def InfosForArchiv(self):
        return DateTime(self.CreationDate()).strftime('%m/01/%Y')

    def getAttendeesOrUsers(self):
        if self.getMeeting_type() == 'poodle_additional':
            users = list(set(self.getUsers() + [a.get('contact', '') for a in self.getResponsibility()]))
            return users
        elif self.getMeeting_type() == 'meeting_dates_additional':
            users = list(set([a.get('contact', '') for a in self.getAttendees()] + [a.get('contact', '') for a in self.getResponsibility()]))
            return users
        else:
            return [a.get('contact', '') for a in self.getResponsibility()]


    def getMeetingTypes(self):
        return atapi.DisplayList((
                                 ('dates_additional', _(u'meeting_type_event')),
                                 ('poodle_additional', _(u'meeting_type_survey')),
                                 ('meeting_dates_additional', _(u'meeting_type_meeting')),
                                ))

    def getMeetingForms(self):
        values = atapi.DisplayList()
        if self.portal_properties.get('izug_meeting_properties'):
            for item in getattr(self.portal_properties.get('izug_meeting_properties'), 'meeting_form'):
                values.add(item, item)
        return values.sortedByValue()

    #makes ical export work
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


atapi.registerType(Meeting, PROJECTNAME)
