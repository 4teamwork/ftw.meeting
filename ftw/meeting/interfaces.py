from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Interface


class IMeetingItem(Interface):
    """A type for meeting items."""


class IMeeting(Interface):
    """A type for meetings."""


class IResponsibilityInfoGetter(Interface):
    """Inteface for ResponsibilityInfoGetter utilities"""


class IMeetingLayer(IDefaultPloneLayer):
    """Themelayer for Meeting"""
