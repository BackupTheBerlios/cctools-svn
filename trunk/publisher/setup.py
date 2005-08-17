"""
P6

Nathan R. Yergler

$Id$
"""

import os
import sys
import shutil
import fnmatch
import platform

from distutils.core import setup, Extension
from distutils import sysconfig
from distutils.command import build_scripts, install_data, build_ext
from distutils.errors import CompileError

extensions = [Extension('zope.proxy._zope_proxy_proxy',
                        ['zope/proxy/_zope_proxy_proxy.c'],
                        include_dirs=[os.path.join('.','zope','proxy')],
                        )
              ]

setup(name='P6',
      version=1.9,
      description = "Desktop tools for licensing works and uploading to the "
                    "Internet Archive for hosting and cataloging.",
      long_description="",
      url='http://creativecommons.org',
      author='Nathan R. Yergler',
      author_email='nathan@creativecommons.org',
      py_modules=['setup', ],
      ext_modules=extensions,
      packages=['p6', 'p6.app', 'p6.configure',
                'p6.metadata', 
                'p6.storage','p6.storage.providers',
                'p6.ui', 'p6.ui.pages',
                'p6.zcmlsupport',
                'pyarchive', 'zope',
                'zope.component', 'zope.component.bbb',
                'zope.component.bbb.tests',
                'zope.configuration', 'zope.deprecation',
                'zope.event', 'zope.exceptions',
                'zope.i18n', 'zope.i18n.interfaces', 
                'zope.i18nmessageid', 'zope.interface',
                'zope.interface.common',
                'zope.modulealias', 'zope.proxy', 'zope.schema',
                'zope.testing',],
      )
    
