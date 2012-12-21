from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content import folder
from Products.ATReferenceBrowserWidget import ATReferenceBrowserWidget
from Products.Archetypes import atapi
from ftw.meeting import meetingMessageFactory as _
from ftw.meeting.config import PROJECTNAME
from ftw.meeting.interfaces import IMeetingItem
from zope.interface import implements


MeetingItemSchema = folder.ATFolderSchema.copy() + atapi.Schema((

        atapi.LinesField(
            name='responsibility',
            required=False,
            searchable=True,
            index='KeywordIndex:schema',
            vocabulary_factory='ftw.meeting.users',

            widget=atapi.MultiSelectionWidget(
                label=_(u"meetingitem_label_responsibility",
                        default=u"Responsibility"),
                description=_(u"meetingitem_help_responsibility",
                              default=u"Select the responsible person(s)."),
                size=4,
                format='checkbox')),

        atapi.TextField(
            name='text',
            searchable=True,
            required=False,
            primary=True,
            default_content_type='text/html',
            allowable_content_types=('text/html',),
            validators=('isTidyHtmlWithCleanup', ),
            default_output_type='text/x-html-safe',
            default_input_type='text/html',
            storage=atapi.AnnotationStorage(),
            widget=atapi.RichWidget(
                label=_(u"meetingitem_label_text", default=u"Text"),
                description=_(u"meetingitem_help_text",
                              default=u"Enter the text."),
                rows=10)),

        atapi.TextField(
            name='conclusion',
            searchable=True,
            required=False,
            primary=False,
            default_content_type='text/html',
            allowable_content_types=('text/html',),
            validators=('isTidyHtmlWithCleanup', ),
            default_output_type='text/x-html-safe',
            default_input_type='text/html',
            storage=atapi.AnnotationStorage(),
            widget=atapi.RichWidget(
                label=_(u"meetingitem_label_conclusion",
                        default=u"Conclusion"),
                description=_(
                    u"meetingitem_help_conclusion",
                    default=u"Enter the conclusion drawn for this resolution"),
                rows=10)),

        atapi.ReferenceField(
            name='related_items',
            relationship='relatesTo',
            multiValued=True,
            isMetadata=True,
            languageIndependent=False,

            widget=ATReferenceBrowserWidget.ReferenceBrowserWidget(
                label=_(u"meeting_label_related_items",
                        default=u"Related Items"),
                description=_(u"meeting_help_related_items",
                              default=u""),
                allow_search=True,
                allow_browse=True,
                show_indexes=False,
                force_close_on_insert=False,
                visible={'edit': 'visible', 'view': 'invisible'})),

        ))


# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

MeetingItemSchema['description'].widget.visible = {'view': 'invisible',
                                                   'edit': 'invisible'}
MeetingItemSchema.changeSchemataForField('effectiveDate', 'settings')
MeetingItemSchema.changeSchemataForField('expirationDate', 'settings')
MeetingItemSchema['effectiveDate'].widget.visible = {'view': 'invisible',
                                                     'edit': 'invisible'}
MeetingItemSchema['expirationDate'].widget.visible = {'view': 'invisible',
                                                      'edit': 'invisible'}


class MeetingItem(folder.ATFolder):
    """A type for meeting items."""
    implements(IMeetingItem)
    security = ClassSecurityInfo()

    portal_type = "Meeting Item"

    schema = MeetingItemSchema

    text = atapi.ATFieldProperty('text')
    conclusion = atapi.ATFieldProperty('conclusion')

    security.declarePublic('canSetDefaultPage')
    def canSetDefaultPage(self):
        return False


atapi.registerType(MeetingItem, PROJECTNAME)
