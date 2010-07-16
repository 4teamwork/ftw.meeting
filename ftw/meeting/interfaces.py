from zope.interface import Interface

class IMeetingItem(Interface):
    """A type for meeting items."""

class IMeeting(Interface):
    """A type for meetings."""

class IResponsibilityInfoGetter(Interface):
    """Inteface for ResponsibilityInfoGetter utilities
    """