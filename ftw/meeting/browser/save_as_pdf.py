from Acquisition import aq_inner
from Acquisition import aq_parent
from ftw.meeting import _
from ftw.pdfgenerator.interfaces import IPDFAssembler
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import getMultiAdapter


class SaveAsPDF(BrowserView):
    """Meeting View
    """

    CONTENTTYPE = 'File'
    PREFIX = 'pdf_'

    def __call__(self):
        self.save_as_pdf()

        return self.request.response.redirect(
            aq_inner(self.context).absolute_url())

    def save_as_pdf(self):
        pdf_data = self._get_pdf_data()
        pdf = self._create_pdf_object(pdf_data)
        self._set_related_items(pdf)
        self._add_portal_message()

        return pdf

    def _create_pdf_object(self, data):
        title = self.context.Title()
        pdf_id = self._parent.invokeFactory(
            self.CONTENTTYPE, self._get_id(),
            title=title)
        pdf = self._parent.get(pdf_id)
        pdf.setFile(data)
        pdf.getFile().setFilename('{0}.pdf'.format(title))

        pdf.processForm()

        return pdf

    def _set_related_items(self, item):
        self.context.setRelated_items(
            self.context.getRelated_items() + [item])

    def _add_portal_message(self):
        msg = _(u'message_pdf_creation_was_successfully',
                'PDF creation was successfully.')
        IStatusMessage(self.request).addStatusMessage(msg, type='info')

    def _get_id(self):
        base_id = new_id = self.PREFIX + self.context.getId()
        counter = 0
        while new_id in self._parent.objectIds():
            counter += 1
            new_id = '{0}-{1}'.format(base_id, counter)

        return new_id

    def _get_pdf_data(self):
        return getMultiAdapter(
            (self.context, self.request), IPDFAssembler).build_pdf()

    @property
    def _parent(self):
        return aq_parent(aq_inner(self.context))
