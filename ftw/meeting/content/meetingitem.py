from ftw.meeting import meetingMessageFactory as _
from ftw.meeting.config import PROJECTNAME
from ftw.meeting.interfaces import IMeetingItem
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from zope.interface import implements

MeetingItemSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    atapi.LinesField(
        'responsibility',
        required = False,
        searchable = True,
        index = 'KeywordIndex:schema',
        vocabulary_factory = 'ftw.meeting.users',
        storage = atapi.AnnotationStorage(),
        widget = atapi.MultiSelectionWidget(
            size = 4,
            label = _(
                u"meetingitem_label_responsibility",
                default=u"Responsibility"),
            description = _(
                u"meetingitem_help_responsibility",
                default=u"Select the responsible person(s)."),
            format='checkbox',
        ),
    ),

    atapi.TextField(
        'text',
        searchable = True,
        required = False,
        primary = True,
        default_content_type = 'text/html',
        default_output_type = 'text/html',
        storage = atapi.AnnotationStorage(),
        widget = atapi.RichWidget(
            label=_(u"meetingitem_label_text", default=u"Text"),
            description=_(u"meetingitem_help_text",
                default=u"Enter the text."),
            rows=10,
        ),
    ),

    atapi.TextField(
    'conclusion',
        searchable = True,
        required = False,
        primary = False,
        default_content_type = 'text/html',
        default_output_type = 'text/html',
        storage = atapi.AnnotationStorage(),
        widget = atapi.RichWidget(
            label = _(u"meetingitem_label_conclusion", default=u"Conclusion"),
            description = _(
                u"meetingitem_help_conclusion",
                default=u"Enter the conclusion drawn for this resolution"),
            rows=10,
        ),
    ),
))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

MeetingItemSchema['title'].storage = atapi.AnnotationStorage()
MeetingItemSchema['description'].storage = atapi.AnnotationStorage()
MeetingItemSchema['description'].widget.visible = {'view': 'invisible',
                                                   'edit': 'invisible'}
MeetingItemSchema.changeSchemataForField('effectiveDate', 'settings')
MeetingItemSchema.changeSchemataForField('expirationDate', 'settings')
MeetingItemSchema['effectiveDate'].widget.visible = {'view': 'invisible',
                                                     'edit': 'invisible'}
MeetingItemSchema['expirationDate'].widget.visible = {'view': 'invisible',
                                                      'edit': 'invisible'}


# customize relateditems for meeting (ex. diffrent title)
MeetingItemSchema['relatedItems'].schemata = 'additional',
MeetingItemSchema['relatedItems'].storage = atapi.AnnotationStorage()
MeetingItemSchema['relatedItems'].widget.allow_search = True
MeetingItemSchema['relatedItems'].widget.allow_browse = True
MeetingItemSchema['relatedItems'].widget.show_indexes = False
MeetingItemSchema['relatedItems'].widget.force_close_on_insert = False
MeetingItemSchema['relatedItems'].widget.label = _(
    u"meeting_label_related_items",
    default=u"Related Items"),
MeetingItemSchema['relatedItems'].widget.description = _(
    u"meeting_help_related_items",
    default=u""),
MeetingItemSchema['relatedItems'].widget.visible = {'edit': 'visible',
                                                    'view': 'invisible'}


class MeetingItem(folder.ATFolder):
    """A type for meeting items."""
    implements(IMeetingItem)

    portal_type = "Meeting Item"

    schema = MeetingItemSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    duration = atapi.ATFieldProperty('duration')
    responsibility = atapi.ATFieldProperty('responsibility')
    responsibilityString = atapi.ATFieldProperty('responsibilityString')
    text = atapi.ATFieldProperty('text')
    meetingitem_type = atapi.ATFieldProperty('meetingitem_type')
    conclusion = atapi.ATFieldProperty('conclusion')
    related_items = atapi.ATFieldProperty('related_items')

atapi.registerType(MeetingItem, PROJECTNAME)
