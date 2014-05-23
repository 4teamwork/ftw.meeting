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
        related_items = self.context.getRelated_items()

        # The Meeting as pdf
        yield (u'{0}/{1}'.format(
            path_prefix, self._pdf_name),
            StringIO(self._pdf_data))

        # All references
        path_prefix = u'{0}/{1}'.format(path_prefix, self.subfolder_path)
        for obj in related_items:

            # if obj.UID() is self._pdf_representation.UID():
            #     # Skip the own pdf representation reference
            #     continue

            if obj.absolute_url() in self.context.absolute_url():
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
    def _pdf_representation(self):
        pdf = self.context.getPdf_representation()
        if not pdf:
            pdf = self._save_as_pdf_view.save_as_pdf()
        return pdf

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

    @property
    def subfolder_path(self):
        message = _(
            u'meetingreferences_folder',
            default='${title} - references',
            mapping={'title': self.context.Title().decode('utf-8')})

        return translate(message, context=self.context.REQUEST)
