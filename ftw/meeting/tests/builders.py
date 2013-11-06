from ftw.builder import builder_registry
from ftw.builder.archetypes import ArchetypesBuilder


class MeetingBuilder(ArchetypesBuilder):

    portal_type = 'Meeting'

builder_registry.register('meeting', MeetingBuilder)
