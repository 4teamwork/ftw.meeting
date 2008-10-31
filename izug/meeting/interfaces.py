from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from izug.meeting import meetingMessageFactory as _

# -*- extra stuff goes here -*-

class IMeetingItem(Interface):
    """A type for meeting items."""

class IMeeting(Interface):
    """A type for meetings."""
