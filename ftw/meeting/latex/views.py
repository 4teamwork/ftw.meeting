from Products.CMFCore.utils import getToolByName
from ftw.meeting import meetingMessageFactory as _
from ftw.meeting.interfaces import IMeeting, IMeetingItem
from ftw.pdfgenerator.interfaces import ILaTeXLayout
from ftw.pdfgenerator.view import MakoLaTeXView
from ftw.pdfgenerator.view import RecursiveLaTeXView
from zope.component import adapts
from zope.i18n import translate
from zope.i18nmessageid import Message
from zope.interface import Interface


class MeetingView(RecursiveLaTeXView):
    adapts(IMeeting, Interface, ILaTeXLayout)

    template_directories = ['templates']
    template_name = 'meeting.tex'

    def get_render_arguments(self):
        meeting = self.context
        args = super(MeetingView, self).get_render_arguments()

        args.update({
                '_': lambda *a, **kw: translate(_(*a, **kw),
                                                context=self.request),
                'title': meeting.Title(),
                'meetingForm': '',
                'metadata': self.get_metadata(),
                'meetingItems': None})

        if meeting.getMeeting_type() == 'meeting':
            args['meetingForm'] = self._get_meeting_value('meeting_form')
            args['meetingItems'] = self.get_meeting_item_titles()

        return args

    def get_metadata(self):
        metadata = []

        metadata.extend(self.get_dates_metadata())

        metadata.append((_(u'meeting_label_location', default=u'Location'),
                         self._get_meeting_value('location')))

        if self.context.getMeeting_type() == 'meeting':
            metadata.extend(self.get_meeting_metadata())

        return self._translate_metadata_labels(metadata)

    def get_meeting_metadata(self):
        metadata = []

        metadata.append((_(u'meeting_label_head_of_meeting',
                           default=u'Head of Meeting'),
                         self._get_meeting_value('head_of_meeting')))

        metadata.append((_(u'meeting_label_recording_secretary',
                           default=u'Recording Secretary'),
                         self._get_meeting_value('recording_secretary')))

        metadata.append(('', ''))

        metadata.append((_(u'meeting_label_attendees', default=u'Attendees'),
                         self.get_meeting_attendees()))

        metadata.append(('', ''))

        return metadata

    def get_dates_metadata(self):
        metadata = []
        meeting = self.context
        convert = self.convert
        translation = getToolByName(self.context, 'translation_service')
        localize_time = translation.ulocalized_time

        start_date = localize_time(meeting.start_date, long_format=False)
        start_time = localize_time(meeting.start_date, time_only=True)
        start = localize_time(meeting.start_date, long_format=True)

        end_date = localize_time(meeting.end_date, long_format=False)
        end_time = localize_time(meeting.end_date, time_only=True)
        end = localize_time(meeting.end_date, long_format=True)

        if start_date == end_date:
            metadata.append((_(u'latex_date', default=u'Date'),
                             convert(start_date)))
            metadata.append((_(u'latex_duration', default=u'Duration'),
                             '%s\,--\,%s' % (convert(start_time),
                                             convert(end_time))))

        else:
            metadata.append((_(u'latex_start', default=u'Start'),
                             convert(start)))
            metadata.append((_(u'latex_end', default=u'End'),
                             convert(end)))

        return metadata

    def get_meeting_attendees(self):
        items = []
        attendees_voc = self.context.getAttendeesVocabulary()
        present_voc = self.context.getPresentOptions()

        for attendee in self.context.getAttendees():
            name = attendees_voc.getValue(attendee['contact'])
            if isinstance(name, str):
                name = name.decode('utf-8')
            items.append(r'%s, %s' % (
                    name,
                    translate(present_voc.getValue(attendee['present']),
                              context=self.request)))

        return r' \newline '.join(items)

    def get_meeting_item_titles(self):
        items = []

        for item in self.context.getFolderContents(
            contentFilter={'portal_type': ['Meeting Item']}):
            items.append(self.convert(item.Title))

        return items

    def _get_meeting_value(self, fieldname):
        field = self.context.getField(fieldname)
        value = field.get(self.context)

        vocabulary = field.Vocabulary(self.context)
        if vocabulary:
            return self.convert(self.context.displayValue(vocabulary, value))
        else:
            return self.convert(value)

    def _translate_metadata_labels(self, metadata):
        new_metadata = []

        for label, value in metadata:
            if isinstance(label, Message):
                label = translate(label, context=self.request)
            new_metadata.append((label, value))

        return new_metadata


class MeetingItemView(MakoLaTeXView):
    adapts(IMeetingItem, Interface, ILaTeXLayout)

    template_directories = ['templates']
    template_name = 'meetingitem.tex'

    def get_render_arguments(self):
        args = super(MeetingItemView, self).get_render_arguments()

        args.update({
                '_': lambda *a, **kw: translate(_(*a, **kw),
                                                context=self.request),
                'title': self.convert(self.context.Title()),
                'responsibles': self.get_responsibles(),
                'text': self.convert(self.context.getText()),
                'conclusion': self.convert(self.context.getConclusion()),
                'relatedItems': self.get_related_items(),
                })

        return args

    def get_responsibles(self):
        responsibles = []

        field = self.context.getField('responsibility')
        vocabulary = field.Vocabulary(self.context)

        for user in self.context.getResponsibility():
            responsibles.append(self.convert(
                    self.context.displayValue(
                        vocabulary, user)))

        return responsibles

    def get_related_items(self):
        items = []

        for obj in self.context.getRelated_items():
            items.append({
                    'title': self.convert(obj.Title()),
                    'url': self.convert(obj.absolute_url())})

        return items
