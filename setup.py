# -*- coding: utf-8 -*-
"""
This module contains the tool of izug.meeting
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.0'

long_description = (
    read('README.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('izug', 'meeting', 'README.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
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
      author='Christian Schneider, 4teamwork GmbH',
      author_email='christian.schneider@4teamwork.ch',
      url='https://svn.4teamwork.ch/repos/zug/izug.meeting',
      license='Copyright 2008, 4teamwork GmbH',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['izug', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
#                        'Products.DataGridField',
#                        'plonegov.pdflatex',
#                        'izug.file',
#                        'izug.task',
#                        'izug.bibliothek',
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'izug.meeting.tests.test_docs.test_suite',
      entry_points="""
      # -*- entry_points -*- 
      [distutils.setup_keywords]
      paster_plugins = setuptools.dist:assert_string_list

      [egg_info.writers]
      paster_plugins.txt = setuptools.command.egg_info:write_arg
      """,
      paster_plugins = ["ZopeSkel"],
      )
