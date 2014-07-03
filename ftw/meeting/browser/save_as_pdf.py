from Acquisition import aq_inner
from Acquisition import aq_parent
from ftw.meeting import _
from ftw.pdfgenerator.interfaces import IPDFAssembler
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import getMultiAdapter


CONTENTTYPE = 'File'
PREFIX = 'pdf_'


class SaveAsPDF(BrowserView):
    """View to create a pdf version of the meeting
    and save it as a sister node.
    """
    def __call__(self):
        self.save_as_pdf()

        return self.request.response.redirect(
            aq_inner(self.context).absolute_url())

    def save_as_pdf(self):
        pdf = self._create_pdf_object(self.pdf_data, self.filename)
        self.context.setPdf_representation(pdf)
        self._add_portal_message()

        return pdf

    @property
    def filename(self):
        return '{0}.pdf'.format(self.context.Title())

    @property
    def pdf_data(self):
        return getMultiAdapter(
            (self.context, self.request), IPDFAssembler).build_pdf()

    def _create_pdf_object(self, data, filename):
        pdf_id = self._get_parent.invokeFactory(
            CONTENTTYPE, self._get_id(),
            title=self.context.Title())
        pdf = self._get_parent.get(pdf_id)
        pdf.setFile(data)
        pdf.getFile().setFilename(filename)

        pdf.processForm()

        return pdf

    def _add_portal_message(self):
        msg = _(u'message_pdf_creation_was_successfully',
                'PDF creation was successfully.')
        IStatusMessage(self.request).addStatusMessage(msg, type='info')

    def _get_id(self):
        base_id = new_id = PREFIX + self.context.getId()
        counter = 0
        while new_id in self._get_parent.objectIds():
            counter += 1
            new_id = '{0}-{1}'.format(base_id, counter)

        return new_id

    @property
    def _get_parent(self):
        return aq_parent(aq_inner(self.context))
