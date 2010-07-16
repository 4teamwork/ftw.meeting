from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope import schema, component
from zope.app.component.hooks import getSite


class AvailableUsersVocabulary(object):
    """
    lists all available users
    """
    
    implements(IVocabularyFactory)
    
    def __call__(self, context):
        """this utility calls plone.principalsource.Users utility
        so we can overwrite this one if we want a diffrent source.
        """ 
        if context is None:
            context = getSite()
        factory = component.getUtility(schema.interfaces.IVocabularyFactory, name='plone.principalsource.Users', context=context)
        items = factory(context)
        return items

AvailableUsersVocabularyFactory = AvailableUsersVocabulary()