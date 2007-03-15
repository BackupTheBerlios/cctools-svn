"""
CC Command Line Tools build script
Builds platform appropriate packages for distribution.

Nathan R. Yergler <nathan@creativecommons.org

$Id: setup_cli.py,v 1.1.1.1 2005/01/04 21:50:03 nyergler Exp $
"""

import os
import sys
import shutil
import fnmatch

try:
    from setuptools import setup
except ImportError, e:
    from distutils.core import setup

# check for win32 support
if sys.platform == 'win32':
    # win32 allows building of executables
    import py2exe

# call the standard distutils builder for the CLI apps 
setup(name='cc_cli_tools',
      version='1.1a1',
      url='http://wiki.creativecommons.org/Command_Line_Tools',
      author='Nathan R. Yergler',
      author_email='nathan@creativecommons.org',

      packages = ['cc_cli_tools'],

      install_requires = ['setuptools',
                          'rdflib==2.3.3',
                          'ccrdf>=0.6a4',
                          'cctagutils>=0.5a2',
                         ],
      include_package_data = True,
      zip_safe = False,

      entry_points = {
    'console_scripts':['ccl = cc_cli_tools.ccl:main',
                       'cct = cc_cli_tools.cct:main',
                       'claim = cc_cli_tools.claim:main'],
    },
      
      )

