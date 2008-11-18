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

from izug.meeting import meetingMessageFactory as _
from izug.meeting.interfaces import IMeetingItem
from izug.meeting.config import PROJECTNAME

MeetingItemSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    atapi.IntegerField('duration',
                       storage = atapi.AnnotationStorage(),
                       widget = atapi.IntegerWidget(label = _(u"meetingitem_label_duration", default=u"Duration"),
                                                    description = _(u"meetingitem_help_duration", default=u"Duration of this item in minutes."),
                                                    ),
                      ),

    atapi.StringField('responsibility',
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

    atapi.ReferenceField('categories',
                         required = False,
                         storage = atapi.AnnotationStorage(),
                         widget=ReferenceBrowserWidget(
                                                       label=_(u"meetingitem_label_categories", default=u"Categories"),
                                                       description=_(u"meetingitem_help_categories", default=u""),
                                                       allow_browse=False,
                                                       show_results_without_query=True,
                                                       restrict_browsing_to_startup_directory=True,
                                                       base_query={"portal_type": "Blog Catgory", "sort_on": "sortable_title"},
                                                       macro='category_reference_widget',
                                                       ),
                         allowed_types=('ClassificationItem',),
                         multiValued=1,
                         schemata='default',
                         relationship='blog_categories'
                         ),

    atapi.LinesField('tags',
                     multiValued=1,
                     storage = atapi.AnnotationStorage(),
                     vocabulary='getAllTags',
                     schemata='default',
                     widget=AddRemoveWidget(
                                            label=_(u"meetingitem_label_tags", default=u"Tags"),
                                            description=_(u"meetingitem_help_tags", default=u"")
                                            ),
                     ),
))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

MeetingItemSchema['title'].storage = atapi.AnnotationStorage()
MeetingItemSchema['description'].storage = atapi.AnnotationStorage()
MeetingItemSchema['description'].widget.visible = {'view' : 'invisible', 'edit' : 'invisible'}

schemata.finalizeATCTSchema(MeetingItemSchema, moveDiscussion=False)

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
    categories = atapi.ATFieldProperty('categories')
    tags = atapi.ATFieldProperty('tags')

    #returns the category uid and the parent category uid
    def getCategoryUids(self):
        cats = aq_inner(self).getCategories()
        uids = [c.UID() for c in cats]
        parent_uids = []
        for pc in cats:
            parent = aq_inner(pc).aq_parent
            puid = parent.UID()
            grand_parent = aq_inner(parent).aq_parent
            if puid not in parent_uids and grand_parent.Type()=='Blog Category':
                parent_uids.append(puid)
                DateTime(self.CreationDate()).strftime('%m/%Y')
        return parent_uids + uids
    
    def getAllTags(self):
        catalog = getToolByName(self, "portal_catalog")
        items = atapi.DisplayList(())
        for i in catalog.uniqueValuesFor("getTags"):
            if i and type(i)==type(''):
                items.add(i,i)
        return items

    def InfosForArchiv(self):
        return DateTime(self.CreationDate()).strftime('%m/01/%Y')

atapi.registerType(MeetingItem, PROJECTNAME)
