from ftw.builder import Builder
from ftw.builder import create
from ftw.meeting.testing import FTW_MEETING_INTEGRATION_TESTING
from ftw.zipexport.interfaces import IZipRepresentation
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from unittest2 import TestCase
from zope.component import getMultiAdapter


class TestMeetingRepresentation(TestCase):

    layer = FTW_MEETING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

    def test_meeting_have_file_representation(self):
        meeting = create(Builder('meeting'))
        zip_repr = getMultiAdapter(
            (meeting, self.request), interface=IZipRepresentation)

        self.assertTrue(zip_repr)

    def test_put_pdf_repr_in_zip_root(self):
        meeting = create(Builder('meeting').titled('J\xc3\xa4mes'))
        zip_repr = getMultiAdapter(
            (meeting, self.request), interface=IZipRepresentation)

        self.assertEqual(
            [(u'/J\xe4mes.pdf')],
            [path for path, stream in zip_repr.get_files()])

    def test_put_all_references_in_a_subfolder(self):
        file_1 = create(Builder('file')
                        .attach_file_containing('My File', 'file_1.doc'))
        file_2 = create(Builder('file')
                        .attach_file_containing('My File', 'file_2.doc'))

        meeting = create(Builder('meeting')
                         .titled('J\xc3\xa4mes')
                         .having(related_items=[file_1, file_2]))

        zip_repr = getMultiAdapter(
            (meeting, self.request), interface=IZipRepresentation)

        self.assertItemsEqual(
            [
                u'/J\xe4mes.pdf',
                u'/J\xe4mes - references/file_1.doc',
                u'/J\xe4mes - references/file_2.doc'
            ],
            [path for path, stream in zip_repr.get_files()])

    def test_do_not_save_a_new_pdf_repr_if_already_one_exists(self):
        meeting = create(Builder('meeting').titled('J\xc3\xa4mes'))
        zip_repr = getMultiAdapter(
            (meeting, self.request), interface=IZipRepresentation)

        tuple(zip_repr.get_files())
        pdf_representation = meeting.getPdf_representation()
        tuple(zip_repr.get_files())

        self.assertEqual(
            pdf_representation,
            meeting.getPdf_representation(),
            'If pdf representation already exists, do not create a new one.')

    def test_always_generate_a_new_pdf_repr_for_the_export(self):
        meeting = create(Builder('meeting').titled('J\xc3\xa4mes'))
        zip_repr = getMultiAdapter(
            (meeting, self.request), interface=IZipRepresentation)

        export_1 = [path for path, stream in zip_repr.get_files()]
        meeting.setTitle('Lara Croft')
        export_2 = [path for path, stream in zip_repr.get_files()]

        self.assertNotEqual(
            export_1,
            export_2,
            'The zipexport should attach always a new pdf-export')

    def test_do_not_break_on_recursion(self):
        folder = create(Builder('folder').having(creators=(u'',)))
        create(Builder('file')
               .attach_file_containing('My File', 'file_1.doc')
               .within(folder))

        # Put the parent as related item
        meeting = create(Builder('meeting')
                         .titled('J\xc3\xa4mes')
                         .within(folder)
                         .having(related_items=[folder]))

        zip_repr = getMultiAdapter(
            (meeting, self.request), interface=IZipRepresentation)

        self.assertEqual(
            [
                u'/J\xe4mes.pdf',
            ],
            [path for path, stream in zip_repr.get_files()])

    def test_export_references_of_meeting_items(self):
        file1 = create(Builder('file')
                       .attach_file_containing('My File', 'file_1.doc'))
        file2 = create(Builder('file')
                       .attach_file_containing('My File', 'file_2.doc'))

        meeting = create(Builder('meeting').titled('J\xc3\xa4mes'))
        create(Builder('meeting item')
               .titled('First meeting item')
               .within(meeting)
               .having(related_items=[file1]))
        create(Builder('meeting item')
               .titled('Second meeting item')
               .within(meeting)
               .having(related_items=[file2]))

        zip_repr = getMultiAdapter(
            (meeting, self.request), interface=IZipRepresentation)

        self.assertItemsEqual(
            [
                u'/J\xe4mes.pdf',
                u'/First meeting item - references/file_1.doc',
                u'/Second meeting item - references/file_2.doc'
            ],
            [path for path, stream in zip_repr.get_files()])
