"""
ccTag build script
Builds platform appropriate packages for distribution.  Takes standard
distutils commands on non-Mac OS X platforms.  Builds a .app on Mac OS X.

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

setup(name='ccPublisher',
      version=1.9,
      description = "Desktop tools for licensing works and uploading to the "
                    "Internet Archive for hosting and cataloging.",
      long_description="",
      url='http://creativecommons.org',
      author='Nathan R. Yergler',
      author_email='nathan@creativecommons.org',
      classifiers= ['Development Status :: 5 - Production/Stable',
                    'Environment :: MacOS X :: Cocoa',
                    'Environment :: Win32 (MS Windows)',
                    'Environment :: X11 Applications :: GTK',
                    'Intended Audience :: End Users/Desktop',
                    'License :: OSI Approved :: GNU General Public License (GPL)',
                    'Natural Language :: English',
                    'Operating System :: OS Independent',
                    'Programming Language :: Python',
                    'Topic :: Multimedia',
                    'Topic :: System :: Archiving',
    ],
      py_modules=['setup', ],
      ext_modules=extensions,
      scripts=['main.py'],
      packages=['ccpublisher', 'ccwsclient', 'ccwx',
                'p6', 'p6.app', 'p6.configure',
                'p6.metadata', 
                'p6.storage',
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

# see if we need to make the disk image
if 'py2app' in sys.argv:
    # create a disk image
    makeDmg([os.path.join('dist', 'ccPublisher.app')],
             os.path.join('build', 'Publisher.dmg'))
    
