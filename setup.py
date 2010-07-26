# -*- coding: utf-8 -*-
"""
This module contains the tool of ftw.meeting
"""
from setuptools import setup, find_packages

def read(*rnames):
    return open('/'.join(rnames)).read()

version = open('ftw/meeting/version.txt').read().strip()
maintainer = 'Mathias Leimgruber'

long_description = (
    read('README.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('docs', 'HISTORY.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('ftw', 'meeting', 'README.txt')
    + '\n' +
    'Download\n'
    '********\n'
    )

tests_require=['zope.testing']

setup(name='ftw.meeting',
      version=version,
      description="Meeting type for ftw",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
      keywords='plone archetype ftw',
      author='%s, 4teamwork GmbH' % maintainer,
      author_email='mailto:info@4teamwork.ch',
      url='http://psc.4teamwork.ch/4teamwork/kunden/ftw/ftw.meeting/',
      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'ftw.calendarwidget',
        'plone.principalsource'
        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'ftw.meeting.tests.test_docs.test_suite',
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
