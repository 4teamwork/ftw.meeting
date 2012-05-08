from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import ViewletBase
from zope.component import getMultiAdapter


class GenerateMeetingViewlet(ViewletBase):
    """Shows a "generate meeting from poodle" button

    """

    render = ViewPageTemplateFile('generate_meeting.pt')

    def __init__(self, *args, **kwargs):
        super(GenerateMeetingViewlet, self).__init__(*args, **kwargs)
        self.poodle_result = None
        self.member = None
        self.options = None

    def update(self):
        """define some values to grap from template"""

        poodle_table = self.context.restrictedTraverse('@@ftw_poodle_table')
        if not poodle_table:
            # ok poodle is not available
            return

        # raw result from poodletable
        # includes a new part results (counted votes per date entry)
        self.poodle_result = poodle_table.poodleResults(print_html=False)

        # options for select input
        options_list = []
        # first iterate throught dates - for the right order
        if self.poodle_result:
            for i, _date in enumerate(self.poodle_result['dates']):
                # dates_record is the correct entry
                # from getDates(datagridfield)
                dates_record = self.context.getDates()[i]
                options_list.append(
                    dict(
                        hash=self.poodle_result['ids'][i],
                        date=dates_record['date'],
                        duration=dates_record['duration'],
                        counter=self.poodle_result['result'][i]))

        self.options = options_list

        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        self.member = portal_state.member()

    def show_generate(self):
        """Decides if the viewlet will be shown or not"""

        # no member
        if not self.member:
            return False

        # no dates in poodle
        if not self.context.getDates():
            return False

        return self.member.id in self.context.Creators() and not \
            self.get_related_meeting()

    def get_related_meeting(self):
        """Returns the first meeting found in related_items, if there's is
        none, return none.

        """

        for obj in self.context.getRelatedItems():
            if obj.portal_type == 'Meeting':
                # check for View permission
                if self.member.has_permission('View', obj):
                    return obj
        return None
