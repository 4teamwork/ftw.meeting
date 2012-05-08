from DateTime import DateTime
from DateTime.interfaces import SyntaxError as DateTimeSyntaxError
from plone.i18n.normalizer import idnormalizer
from Products.Five.browser import BrowserView
from zExceptions import BadRequest
from zope.component import getMultiAdapter
from zope.i18n import translate


# do it like kss, generat our own status message template
status_message_template = lambda msg, mtype: \
    "<dl class='portalMessage %(mtype)s'><dt>%(mtype)s</dt><dd>%(msg)s</dd>" \
    "</dl>" \
    % (dict(mtype=mtype,
            msg=msg))


class CreateMeeting(BrowserView):
    """creates a meeting from poodle informations(data)
    """

    def __call__(self, date_hash=None):
        """If successfull this view returns a small part html
        Example: <a href="url/to/meeting">Meeting</a>
        this will be displayed as statusmessage

        """
        # TODO: Refactor me. Split up into sub methods.

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
        errors = []
        m_title = u"%s %s" % (
            translate(
                'label_create_from_poodle',
                'ftw.meeting',
                context=self.request),
            self.context.Title().decode('utf-8'))
        m_id = idnormalizer.normalize(m_title)

        try:
            parent.invokeFactory('Meeting', m_id)

        except BadRequest:
            # catches duplication error
            return status_message_template(translate(
                    'duplication_error_text',
                    'ftw.meeting',
                    context=self.request),
                                           'error')

        except ValueError:
            # catches "disallowed subobject type"
            return status_message_template(translate(
                    'disallowed_error_text',
                    'ftw_meeting',
                    context=self.request),
                                           'error')
        m_created = getattr(parent, m_id, None)

        #set title and attendees
        m_created.setTitle(m_title)
        m_created.setAttendees(tuple(attendees))
        # try to convert date and duration into DateTime objects
        duration = date_duration['duration'].strip()
        if '-' in duration:
            # expected format HH:MM-HH:MM
            start_time, end_time = duration.split('-')
        # perhaps we should check other time formats
        else:
            #make a reset
            errors.append('wrong_time_format')
            start_time = end_time = '00:00'

        try:
            start = DateTime("%s %s" % (
                    date_duration['date'], start_time))
            m_created.setStart_date(start)
        except DateTimeSyntaxError:
            errors.append('cannot_set_startdate')
        try:
            end = DateTime("%s %s" % (
                    date_duration['date'], end_time))
            m_created.setEnd_date(end)
        except DateTimeSyntaxError:
            errors.append('cannot_set_enddate')

        # set correct meeting type
        m_created.setMeeting_type('meeting')

        # set relation between meeting and poodle
        self.context.setRelatedItems((m_created.UID(), ))

        #finalize
        m_created.processForm()

        # change workflow state from poodle to to close
        context_state = getMultiAdapter(
            (self.context, self.request),
            name=u'plone_context_state')
        if context_state.workflow_state() != 'close':
            tools = getMultiAdapter(
                (self.context, self.request),
                name=u'plone_tools')
            workflow = tools.workflow()
            workflow.doActionFor(
                self.context,
                action='close_poodle',
                wf_id='poodle_workflow')

        if not errors:
            return status_message_template(translate(
                    'meeting_created_text',
                    'ftw.meeting',
                    mapping={'url': m_created.absolute_url(),
                             'title': m_title},
                    context=self.request),
                                           'info')

        else:
            # there were porblems during creation precess
            # TODO: Implement a better error message from error list
            return status_message_template(translate(
                    'meeting_created_text_with_errors',
                    'ftw.meeting',
                    mapping={
                        'url': m_created.absolute_url(),
                        'title': m_title},
                    context=self.request),
                                           'error')
