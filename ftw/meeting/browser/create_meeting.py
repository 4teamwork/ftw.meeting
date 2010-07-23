from Products.Five.browser import BrowserView
from zope.i18n import translate
from DateTime import DateTime
from plone.i18n.normalizer import idnormalizer
from zExceptions import BadRequest


class CreateMeeting(BrowserView):
    """creates a meeting from poodle informations(data)

    """

    def __call__(self, date_hash=None):
        """If successfull this view returns a small part html
        Example: <a href="url/to/meeting">Meeting</a>
        this will be displayed as statusmessage

        """

        if date_hash is None:
            # we cannot do anything
            return

        poodle_data = self.context.getPoodleData()
        parent = self.context.aq_parent
        # all based on the order of entries in dates, ids and poodle entries
        # so get the right index, depending on has_date
        index = poodle_data['ids'].index(date_hash)
        # get all necessary infos
        date_duration = self.context.getDates()[index]
        attendees = []
        # get all available attendees
        for userid, user_dates in poodle_data['users'].items():
            if user_dates[date_hash]:
                attendees.append(dict(contact=userid))

        # create meeting as sibling of poodle
        errors = {}
        m_title = u"%s %s" % (
            translate('label_create_from_poodle', 'ftw.meeting'),
            self.context.Title().decode('utf-8'))
        m_id = idnormalizer.normalize(m_title)
        try:
            parent.invokeFactory('Meeting', m_id)
        except BadRequest:
            # catches duplication error
            return translate('duplication_error_text', 'ftw_meeting')
        except ValueError:
            # catches "disallowed subobject type"
            return translate('dissalowed_error_text', 'ftw_meeting')
        m_created = getattr(parent, m_id, None)

        #set title and attendees
        m_created.setTitle(m_title)
        m_created.setAttendees(tuple(attendees))
        # try to convert date and duration into DateTime objects
        duration = date_duration['duration'].strip()
        if '-' in duration:
            start_time, end_time = duration.split('-')
        # perhaps we should check other time formats
        else:
            #make a reset
            start_time = end_time = '00:00'

        try:
            start = DateTime("%s %s" % (
                date_duration['date'], start_time))
            m_created.setStart_date(start)
        except SyntaxError:
            errors.append('cannot_set_startdate')
        try:
            end = DateTime("%s %s" % (
                date_duration['date'], end_time))
            m_created.setEnd_date(end)
        except SyntaxError:
            errors.append('cannot_set_enddate')

        # set correct meeting type
        m_created.setMeeting_type('meeting_dates_additional')

        #finalize
        m_created.processForm()
        if not errors:
            return translate(
                'meeting_created_text',
                'ftw.meeting',
                mapping={'url': m_created.absolute_url(), 'title': m_title})

        else:
            # there were porblems during creation precess
            return translate(
                'meeting_created_text_with_errors',
                'ftw.meeting',
                mapping={
                    'url': m_created.absolute_url(),
                    'title': m_title,
                    'errors' : [e+", " for e in errors]})
