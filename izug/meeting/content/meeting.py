"""Definition of the Meeting content type
"""

from zope.interface import implements, directlyProvides
from Acquisition import aq_inner, aq_parent

from Products.CMFCore.utils import getToolByName

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.AddRemoveWidget import AddRemoveWidget
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from DateTime import DateTime

from DateTime.DateTime import DateTime
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.CheckboxColumn import CheckboxColumn
from Products.DataGridField.SelectColumn import SelectColumn

from izug.arbeitsraum.content.utilities import finalizeIzugSchema

from izug.meeting import meetingMessageFactory as _
from izug.meeting.interfaces import IMeeting
from izug.meeting.config import PROJECTNAME

from zope.component import getMultiAdapter, queryMultiAdapter, queryUtility
from izug.arbeitsraum.interfaces import IArbeitsraumUtils

from izug.poodle.content.poodle import Poodle,PoodleSchema
from izug.poodle.interfaces import IPoodle


MeetingSchema = folder.ATFolderSchema.copy() + atapi.Schema((

     atapi.LinesField('meeting_type',
                      searchable = False,
                      schemata = 'default',
                      required = True,
                      default="dates_additional",
                      vocabulary = 'getMeetingTypes',
                      storage = atapi.AnnotationStorage(),
                      widget = atapi.SelectionWidget(label = _(u"meeting_label_type", default=u"Event type"),
                                                     description = _(u"meeting_help_type", default=u"Choose your event type."),
                                                     helper_js = ['meeting_toggle_date.js',],
                                                     format='radio',
                                                     ),
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
                  columns = ('contact', 'present','excused'),
                  allow_empty_rows = False,
                  storage = atapi.AnnotationStorage(),
                  widget = DataGridWidget(label = _(u"meeting_label_attendees", default=u"Attendees"),
                                          description = _(u"meeting_help_attendees", default=u"Enter the attendees of the meeting."),
                                          auto_insert = True,
                                          columns = {'contact' : SelectColumn(title = _(u"meeting_label_attendees_attendee", default=u"Attendee"),
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
                         storage = atapi.AnnotationStorage(),
                         widget = ReferenceBrowserWidget(
                                                         allow_search = True,
                                                         allow_browse = True,
                                                         show_indexes = False,
                                                         force_close_on_insert = True,
                                                         label = _(u"meeting_label_related_items", default=u"Related Items"),
                                                         description = _(u"meeting_help_related_items", default=u""),
                                                         visible = {'edit' : 'visible', 'view' : 'invisible' }
                                                         ),
                         ),

)) + PoodleSchema.copy()

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

MeetingSchema['title'].storage = atapi.AnnotationStorage()
MeetingSchema['description'].storage = atapi.AnnotationStorage()
MeetingSchema['description'].required = True

#Poodle "real" integration
MeetingSchema.changeSchemataForField('users','poodle')
MeetingSchema['users'].required = False
MeetingSchema.changeSchemataForField('dates','poodle')


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


class Meeting(folder.ATFolder, Poodle):
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
    attendees = atapi.ATFieldProperty('attendees')
    related_items = atapi.ATFieldProperty('related_items')

    def getAssignableUsers(self):
        """Collect users with a given role and return them in a list.
        """
        a_util = queryUtility(IArbeitsraumUtils,name="arbeitsraum-utils")
        if not a_util:
            return (atapi.DisplayList())
        results = atapi.DisplayList()
        results.add('',_(u'Choose a person'))
        return (results + atapi.DisplayList(a_util.getAssignableUsers(self,'Reader')))
        

    def InfosForArchiv(self):
        return DateTime(self.CreationDate()).strftime('%m/01/%Y')

    def getMeetingTypes(self):
        return atapi.DisplayList((
                                 ('dates_additional',_(u'meeting_type_event')),
                                 ('poodle_additional',_(u'meeting_type_survey')),
                                 ('meeting_dates_additional',_(u'meeting_type_meeting')),
                                ))

atapi.registerType(Meeting, PROJECTNAME)
