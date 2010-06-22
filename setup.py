# -*- coding: utf-8 -*-
"""
This module contains the tool of izug.meeting
"""
from setuptools import setup, find_packages

def read(*rnames):
    return open('/'.join(rnames)).read()

version = open('izug/meeting/version.txt').read().strip()
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
    read('izug', 'meeting', 'README.txt')
    + '\n' +
    'Download\n'
    '********\n'
    )

tests_require=['zope.testing']

setup(name='izug.meeting',
      version=version,
      description="Meeting type for iZug",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
      keywords='plone archetype izug',
      author='%s, 4teamwork GmbH' % maintainer,
      author_email='mailto:info@4teamwork.ch',
      url='http://psc.4teamwork.ch/4teamwork/kunden/izug/izug.meeting/',
      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['izug', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'plonegov.pdflatex',
        'izug.bibliothek',
        # 'Products.DataGridField',
        # 'plonegov.pdflatex',
        # 'izug.file',
        # 'izug.task',
        # 'izug.bibliothek',
        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'izug.meeting.tests.test_docs.test_suite',
      entry_points="""""",
      )
