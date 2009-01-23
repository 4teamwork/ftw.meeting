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

MeetingSchema = folder.ATFolderSchema.copy() + atapi.Schema((

     atapi.BooleanField('no_date',
                      searchable = False,
                      schemata = 'default',
                      default = False,
                      index = 'KeywordIndex:schema',               
                      storage = atapi.AnnotationStorage(),
                      widget = atapi.BooleanWidget(label = _(u"meeting_label_no_date", default=u"Date not yet defined"),
                                                     description = _(u"meeting_help_no_date", default=u"Tick box if you don't know the date yet. For example if you will create a poodle survey."),
                                                     helper_js = ['meeting_toggle_date.js',]
                                                     ),
                      ),

    atapi.DateTimeField('start_date',
                        searchable = True,
                        accessor='start',
                        default_method = DateTime,
                        storage = atapi.AnnotationStorage(),
                        widget = atapi.CalendarWidget(label = _(u"meeting_label_start_date", default=u"Start of Meeting"),
                                                      description = _(u"meeting_help_start_date", default=u"Enter the starting date and time, or click the calendar icon and select it."),
                                                      ),
                        ),


    atapi.DateTimeField('end_date',
                        searchable = True,
                        accessor='end',
                        default_method = DateTime,
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
                                                     'present' : CheckboxColumn(label = _(u"meeting_label_attendees_present", default=u"Present"),
                                                                                ),
                                                     'excused' : CheckboxColumn(label = _(u"meeting_label_attendees_excused", default=u"Excused"),
                                                                                ),
                                                     }
                                          )
                  ),

    atapi.ReferenceField('related_items',
                         relationship = 'relatesTo',
                         multiValued = True,
                         isMetadata = True,
                         languageIndependent = False,
                         index = 'KeywordIndex',
                         accessor = 'relatedItems',
                         storage = atapi.AnnotationStorage(),
                         schemata = 'default',
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

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

MeetingSchema['title'].storage = atapi.AnnotationStorage()
MeetingSchema['description'].storage = atapi.AnnotationStorage()
MeetingSchema['description'].required = True

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
                      storage = atapi.AnnotationStorage(),
                      widget = atapi.StringWidget(label = _(u"meeting_label_location", default=u"Location"),
                                                  description = _(u"meeting_help_location", default=u"Enter the location where the meeting will take place."),
                                                  ),
                      ),
"""

class Meeting(folder.ATFolder):
    """A type for meetings."""
    implements(IMeeting)

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
        return (atapi.DisplayList(a_util.getAssignableUsers(self,'Contributor')))

    def InfosForArchiv(self):
        return DateTime(self.CreationDate()).strftime('%m/01/%Y')

atapi.registerType(Meeting, PROJECTNAME)
