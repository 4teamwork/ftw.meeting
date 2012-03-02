from ftw.meeting import meetingMessageFactory as _
from zope import schema, component
from zope.app.component.hooks import getSite
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


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

        factory = component.queryUtility(
            schema.interfaces.IVocabularyFactory,
            name='assignable_users')

        if factory is None:
            factory = component.getUtility(
                schema.interfaces.IVocabularyFactory,
                name='plone.principalsource.Users', context=context)
        items = factory(context)
        return items


AvailableUsersVocabularyFactory = AvailableUsersVocabulary()


class MeetingTypesVocabulary(object):
    """Vocabulary of available meeting types.
    """

    implements(IVocabularyFactory)

    def __call__(self, context):
        return SimpleVocabulary(tuple(self._get_terms()))

    def _get_terms(self):
        for name, label in self._get_types():
            yield SimpleVocabulary.createTerm(
                name, label, label)

    def _get_types(self):
        return ((u'event', _(u'event', default=u'Event')),
                (u'meeting', _(u'meeting', default=u'Meeting')))


MeetingTypesVocabularyFactory = MeetingTypesVocabulary()
