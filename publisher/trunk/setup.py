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
import sys
import os
import platform
import fnmatch

from deploy.setupsupport import *
from deploy.setupcfg import *

from ccpublisher.const import APPNAME

PLATFORM = platform.system().lower()
RSRC_DIR = 'resources'

# import platform-specific distutils functionality
pkgData = {}
if PLATFORM == 'windows':
    import py2exe
    
elif PLATFORM == 'darwin':
    import py2app
    dataFiles = [('resources', 
                 ['resources/LICENSE.txt', 'resources/wizard.xrc'])] + \
                  findZcml(os.path.dirname(__file__) or os.getcwd())
elif PLATFORM == 'linux':
    from deploy.linux.straw_distutils import setup
    packages = packages + ['deploy', 'deploy.linux']

    pkgData = packageData(packages)
    pkgData.update({'zope.proxy':['proxy.h']})

    RSRC_DIR = 'local/%s/resources' % APPNAME

else:
    print "Unknown platform; unable to continue."
    sys.exit(1)

# fix up the data file inclusion
dataFiles = [(RSRC_DIR, 
             ['resources/LICENSE.txt',
              'resources/wizard.xrc',
              'resources/app.zcml',
	      'resources/ccp8.ico',
	      'resources/cc_33.gif',
	      'resources/version.txt'])
	     ]

if PLATFORM != 'linux':
    # we need to include the ZCML as side-by-side resources on
    # "compiled" platforms
    dataFiles = dataFiles + \
                findZcml(os.path.dirname(__file__) or os.getcwd())
    
if __name__ == '__main__':

    setup(name='ccPublisher',
          version='1.9',
          description = desc,
          long_description= long_desc,
          url='http://creativecommons.org',
          author='Nathan R. Yergler',
          author_email='software@creativecommons.org',
          classifiers= classifiers,
          py_modules=[],
          scripts=['main.py'],
          windows=['main.py'],
          app=['main.py'],
          data_files=dataFiles,
          packages=packages,
          package_data=pkgData,
          options={'py2exe':{'packages':packages,
                             'includes':['dbhash', 'encodings',]
                             },
                   'py2app':{'argv_emulation':True,
			     'iconfile':os.path.join('resources', 'ccp8.icns'),
			     'packages':packages,
                             'includes':['dbhash', 'encodings',]
                             },
                   },
          desktop_file=['deploy/linux/ccpublisher.desktop.in'],
          )
