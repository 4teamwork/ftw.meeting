from ftw.meeting import _
from ftw.meeting.interfaces import IMeeting
from ftw.zipexport.interfaces import IZipRepresentation
from ftw.zipexport.representations.general import NullZipRepresentation
from StringIO import StringIO
from zope.component import adapts
from zope.component import getMultiAdapter
from zope.i18n import translate
from zope.interface import implements
from zope.interface import Interface


class MeetingZipRepresentation(NullZipRepresentation):
    implements(IZipRepresentation)
    adapts(IMeeting, Interface)
    """Exports the meeting as pdf and put all referenced
    items into a subfolder.
    """
    def get_files(self, path_prefix=u"", recursive=True, toplevel=True):

        # The Meeting as pdf
        yield (u'{0}/{1}'.format(
            path_prefix, self._pdf_name),
            StringIO(self._pdf_data))

        # All references of the meeting
        for reference in self.export_references(path_prefix, recursive):
            yield reference

        # All references of meeting items
        query = {'portal_type': 'Meeting Item'}
        meetingitems = self.context.getFolderContents(query, full_objects=True)
        for meetingitem in meetingitems:
            for reference in self.export_references(path_prefix, recursive, meetingitem):
                yield reference

    def export_references(self, path_prefix, recursive, content=None):
        if content is None:
            content = self.context

        related_items = content.getRelated_items()
        path_prefix = u'{0}/{1}'.format(path_prefix,
                                        self.subfolder_path(content))

        for obj in related_items:

            if obj.absolute_url() in content.absolute_url():
                # Prevent unlimited recursion if a related_item is a parent.
                # We just skip this item
                continue

            adapt = getMultiAdapter(
                (obj, self.request),
                interface=IZipRepresentation)

            for item in adapt.get_files(
                path_prefix=path_prefix,
                recursive=recursive,
                toplevel=False
            ):

                yield item

    @property
    def _pdf_data(self):
        return self._save_as_pdf_view.pdf_data

    @property
    def _pdf_name(self):
        return self._save_as_pdf_view.filename.decode('utf-8')

    @property
    def _save_as_pdf_view(self):
        return getMultiAdapter(
            (self.context, self.request), name="save_as_pdf")

    def subfolder_path(self, content):
        message = _(
            u'meetingreferences_folder',
            default='${title} - references',
            mapping={'title': content.Title().decode('utf-8')})

        return translate(message, context=self.context.REQUEST)
