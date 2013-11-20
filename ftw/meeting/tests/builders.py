from ftw.builder import builder_registry
from ftw.builder.archetypes import ArchetypesBuilder


class MeetingBuilder(ArchetypesBuilder):

    portal_type = 'Meeting'

builder_registry.register('meeting', MeetingBuilder)


class MeetingItemBuilder(ArchetypesBuilder):

    portal_type = 'Meeting Item'

builder_registry.register('meeting item', MeetingItemBuilder)


class TaskBuilder(ArchetypesBuilder):

    portal_type = 'Task'

builder_registry.register('task', TaskBuilder)
