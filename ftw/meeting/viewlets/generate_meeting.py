from plone.app.layout.viewlets import ViewletBase
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class GenerateMeetingViewlet(ViewletBase):
    """Shows a "generate meeting from poodle" button

    """
    render = ViewPageTemplateFile('generate_meeting.pt')

    def update(self):
        """define some values to grap from template"""

        poodle_table = self.context.restrictedTraverse('@@ftw_poodle_table')
        if not poodle_table:
            # ok poodle is not available
            return

        # raw result from poodletable
        # includes a new part results (counted votes per date entry)
        self.poodle_result = poodle_table.poodleResults(print_html=False)

        # dict which containes
        options_list = []
        # first iterate throught dates - for the right order
        for i, date in enumerate(self.poodle_result['dates']):
            # dates_record is the correct entry from getDates(datagridfield)
            dates_record = self.context.getDates()[i]
            options_list.append(
                dict(
                    hash=self.poodle_result['ids'][i],
                    date=dates_record['date'],
                    duration=dates_record['duration'],
                    counter=self.poodle_result['result'][i]))

        self.options = options_list


    def show_generate(self):
        """Decides if the viewlet will be shown or not"""
        
        mtool = getToolByName(self.context, "portal_membership")
        member = mtool.getAuthenticatedMember()
        if not member:
            return False
        
        return member.id in self.context.Creators() and not \
            self.get_related_meeting()

        
    def get_related_meeting(self):
        """Returns the first meeting found in related_items, if there's is 
        none, return none.

        """

        for obj in self.context.getRelatedItems():
            if obj.portal_type == 'Meeting':
                return obj
        return None