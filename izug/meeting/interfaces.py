from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from izug.meeting import meetingMessageFactory as _

# -*- extra stuff goes here -*-

class IMeetingLayoutPDF(Interface):
    """Marker Interface: Object is exportable with Meeting Layout definition"""

class IMeetingItem(IMeetingLayoutPDF):
    """A type for meeting items."""

class IMeeting(IMeetingLayoutPDF):
    """A type for meetings."""
