"""Definition of the Meeting Item content type
"""

from zope.interface import implements, directlyProvides
from Acquisition import aq_inner, aq_parent

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.CMFCore.utils import getToolByName

from Products.AddRemoveWidget import AddRemoveWidget
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from DateTime import DateTime

from izug.arbeitsraum.content.utilities import finalizeIzugSchema

from izug.meeting import meetingMessageFactory as _
from izug.meeting.interfaces import IMeetingItem
from izug.meeting.config import PROJECTNAME

MeetingItemSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    atapi.IntegerField('duration',
                       required = True,
                       storage = atapi.AnnotationStorage(),
                       widget = atapi.IntegerWidget(label = _(u"meetingitem_label_duration", default=u"Duration"),
                                                    description = _(u"meetingitem_help_duration", default=u"Duration of this item in minutes."),
                                                    ),
                      ),

    atapi.StringField('responsibility',
                      required = True,
                      storage = atapi.AnnotationStorage(),
                      widget = atapi.StringWidget(label = _(u"meetingitem_label_responsibility", default=u"Responsibility"),
                                                  description = _(u"meetingitem_help_responsibility", default=u"Select the responsible person."),
                                                  ),
                      ),

    atapi.TextField('text',
                    searchable = True,
                    required = False,
                    primary = True,
                    default_content_type = 'text/html',
                    default_output_type = 'text/html',
                    allowable_content_types = ('text/html','text/structured','text/plain',),
                    storage = atapi.AnnotationStorage(),
                    widget = atapi.RichWidget(label=_(u"meetingitem_label_text", default=u"Text"),
                                              description=_(u"meetingitem_help_text", default=u"Enter the text."),
                                              rows=20,
                                              ),
                    ),

    atapi.StringField('meetingitem_type',
                      vocabulary=((
                                   (u"", u""), 
                                   (u"B", u"resolutions"),
                                   (u"I", u"informations"),
                                   (u"M", u"measures"),
                                   )),
                      enforceVocabulary = True,
                      languageIndependent = True,
                      storage = atapi.AnnotationStorage(),
                      widget = atapi.SelectionWidget(label = _(u"meetingitem_label_item_type", default=u"Item type"),
                                                     description = _(u"meetingitem_help_item_type", default=u"Choose the type of the item."),
                                                     format = 'select',
                                                     ),
                      ),

    atapi.TextField('conclusion',
                    searchable = True,
                    required = False,
                    primary = False,
                    default_content_type = 'text/html',              
                    default_output_type = 'text/html',
                    allowable_content_types = ('text/html','text/structured','text/plain',),
                    storage = atapi.AnnotationStorage(),
                    widget = atapi.RichWidget(label = _(u"meetingitem_label_conclusion", default=u"Conclusion"),
                                              description = _(u"meetingitem_help_conclusion", default=u"Enter the conclusion drawn for this resolution"),
                                              rows=20,
                                              ),
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
                                                         label = _(u"meetingitem_label_related_items", default=u"Related Items"),
                                                         description = _(u"meetingitem_help_related_items", default=u""),
                                                         visible = {'edit' : 'visible', 'view' : 'invisible' }
                                                         ),
                         ),
))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

MeetingItemSchema['title'].storage = atapi.AnnotationStorage()
MeetingItemSchema['description'].storage = atapi.AnnotationStorage()
MeetingItemSchema['description'].widget.visible = {'view' : 'invisible', 'edit' : 'invisible'}

finalizeIzugSchema(MeetingItemSchema, moveDiscussion=False)

class MeetingItem(folder.ATFolder):
    """A type for meeting items."""
    implements(IMeetingItem)

    portal_type = "Meeting Item"
    schema = MeetingItemSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    duration = atapi.ATFieldProperty('duration')
    responsibility = atapi.ATFieldProperty('responsibility')
    text = atapi.ATFieldProperty('text')
    meetingitem_type = atapi.ATFieldProperty('meetingitem_type')
    conclusion = atapi.ATFieldProperty('conclusion')
    related_items = atapi.ATFieldProperty('related_items')

    def InfosForArchiv(self):
        return DateTime(self.CreationDate()).strftime('%m/01/%Y')

atapi.registerType(MeetingItem, PROJECTNAME)
