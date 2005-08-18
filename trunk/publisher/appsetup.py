"""
ccTag build script
Builds platform appropriate packages for distribution.  Takes standard
distutils commands on non-Mac OS X platforms.  Builds a .app on Mac OS X.

Nathan R. Yergler

$Id$
"""

from distutils.core import setup, Extension

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
      py_modules=['appsetup', ],
      scripts=['main.py'],
      packages=['ccpublisher', ],
      )
