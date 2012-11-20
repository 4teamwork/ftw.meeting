import unittest2 as unittest
import transaction
from ftw.meeting.testing import FTW_MEETING_FUNCTIONAL_TESTING
from plone.app.testing import login, setRoles
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME, TEST_USER_PASSWORD
from plone.testing.z2 import Browser


class TestDate(unittest.TestCase):

    layer = FTW_MEETING_FUNCTIONAL_TESTING

    def setUp(self):
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        setRoles(portal, TEST_USER_ID, ['Manager'])
        self.browser = Browser(self.layer['app'])
        self.folder = portal[portal.invokeFactory(id='folder',
                                                  type_name='Folder')]
        transaction.commit()

    def _open_url(self, url):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME, TEST_USER_PASSWORD))
        self.browser.open(url)

    def _set_dates(self, start, end):
        s_day, s_month, s_year = start.split('.')
        e_day, e_month, e_year = end.split('.')

        self.browser.getControl(name='start_date_day').getControl(value=s_day).click()
        self.browser.getControl(name='start_date_month').getControl(value=s_month).click()
        self.browser.getControl(name='start_date_year').getControl(value=s_year).click()

        self.browser.getControl(name='end_date_day').getControl(value=e_day).click()
        self.browser.getControl(name='end_date_month').getControl(value=e_month).click()
        self.browser.getControl(name='end_date_year').getControl(value=e_year).click()

    def test_start_before_end(self):
        self._open_url(self.folder.absolute_url() + '/createObject?type_name=Meeting')
        self._set_dates('10.10.2010', '20.12.2012')
        self.browser.getControl(name='title').value = 'Meeting1'
        self.browser.getControl(name='form.button.save').click()
        # Should be in edit
        self.assertEqual(self.folder.meeting1.absolute_url(),
                         self.browser.url.rstrip('/'))


    def test_end_before_start(self):
        self._open_url(self.folder.absolute_url() + '/createObject?type_name=Meeting')
        self._set_dates('20.12.2012', '10.10.2010')
        self.browser.getControl(name='title').value = 'Meeting2'
        self.browser.getControl(name='form.button.save').click()
        # Should be in edit
        self.assertIn('edit', self.browser.url)
        self.assertIn('End date must be after start date.', self.browser.contents)
