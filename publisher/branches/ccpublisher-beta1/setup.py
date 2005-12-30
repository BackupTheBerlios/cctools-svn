"""
ccPublisher Build Script
Builds platform appropriate packages for distribution.

 Windows:
 $ python appsetup.py py2exe

 Mac OS X:
 $ python appsetup.py py2app

 Linux:
 $ python appsetup.py bdist_rpm

copyright 2004-2005, Nathan R. Yergler
licensed to the public under the GNU GPL version 2.

$Id$
"""

from distutils.core import setup, Extension
import os
import platform
import fnmatch

from deploy.setupsupport import *
from deploy.setupcfg import *

PLATFORM = platform.system().lower()

# import platform-specific distutils functionality
if PLATFORM == 'windows':
    import py2exe
elif PLATFORM == 'darwin':
    import py2app
else:
    from deploy.linux.straw_distutils import setup
                    
if __name__ == '__main__':
    
    setup(name='ccPublisher',
          version='1.9',
          description = desc,
          long_description= long_desc,
          url='http://creativecommons.org',
          author='Nathan R. Yergler',
          author_email='software@creativecommons.org',
          classifiers= classifiers,
          py_modules=['setup' ],
          scripts=['main.py'],
          windows=['main.py'],
          app=['main.py'],
          ext_modules=extensions,
          data_files=[('resources', 
                      ['resources/LICENSE.txt', 'resources/wizard.xrc'])] + 
                      findZcml(os.path.dirname(__file__) or os.getcwd()),
          packages=packages,
          package_data=packageData(packages),
          options={'py2exe':{'packages':packages,
                             'includes':['dbhash', 'encodings',]
                             },
                   'py2app':{'packages':packages,
                             'includes':['dbhash', 'encodings',]
                             },
                   },
          desktop_file=['deploy/linux/ccpublisher.desktop.in'],
          )
