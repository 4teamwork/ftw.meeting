from setuptools import setup, find_packages
import os

version = '1.4.6'
maintainer = 'Mathias Leimgruber'

tests_require = [
    'plone.app.testing',
    'ftw.pdfgenerator',
    'ftw.testing',
    'ftw.workspace',
    'ftw.poodle',
    'ftw.builder',
    ]

extras_require = {
    'tests': tests_require,
    'pdf': [
        'ftw.pdfgenerator',
        ],
    'task': [
        'ftw.task']}

setup(name='ftw.meeting',
      version=version,
      description='A meeting content type for Plone.',
      long_description=open('README.rst').read() + '\n' + \
          open(os.path.join('docs', 'HISTORY.txt')).read(),

      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.1',
        'Framework :: Plone :: 4.2',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

      keywords='ftw meeting plone',
      author='4teamwork GmbH',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/ftw.meeting',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw', ],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'Products.DataGridField>=1.9',
        'setuptools',
        'ftw.calendarwidget',
        'plone.principalsource',
        'ftw.upgrade',
        ],

      tests_require=tests_require,
      extras_require=extras_require,

      test_suite = 'ftw.meeting.tests.test_docs.test_suite',
      entry_points='''
      [z3c.autoinclude.plugin]
      target = plone
      ''',
      )
