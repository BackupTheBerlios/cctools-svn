"""
ccTag build script
Builds platform appropriate packages for distribution.  Takes standard
distutils commands on non-Mac OS X platforms.  Builds a .app on Mac OS X.

Nathan R. Yergler

$Id$
"""

from distutils.core import setup, Extension
import os
import platform
import fnmatch

PLATFORM = platform.system().lower()

if PLATFORM == 'windows':
    import py2exe
elif PLATFORM == 'darwin':
    import py2app

def findZcml():
    result = []
    
    basePath = os.getcwd()
    
    for (dirpath, dirnames, filenames) in os.walk(basePath):
        relpath = dirpath[len(basePath)+1:]
        zcml = fnmatch.filter(filenames, "*.zcml")
        
        if len(zcml) > 0:
            result.append((relpath, [os.path.join(relpath, n) for n in zcml]))

    return result

extensions = [Extension('zope.proxy._zope_proxy_proxy',
                        ['zope/proxy/_zope_proxy_proxy.c'],
                        include_dirs=[os.path.join('.','zope','proxy')],
                        )
              ]

packages = ['ccpublisher',
            'p6', 'p6.app', 
            'p6.configure', 'p6.zcmlsupport',
            'p6.metadata', 
            'p6.storage','p6.storage.providers',
            'p6.ui', 'p6.ui.pages', 'p6.ui.windows',
            'pyarchive', 'ccrdf', 'cctagutils', 'tagger', 'ccwsclient',
            'ccwx','eyeD3',
            'rdflib',
            'rdflib.backends',
            'rdflib.syntax',
            'rdflib.syntax.serializers',
            'rdflib.syntax.parsers',
            'rdflib.model',
            'zope',
            'zope.component', 'zope.component.bbb',
            'zope.component.bbb.tests',
            'zope.configuration', 'zope.deprecation',
            'zope.event', 'zope.exceptions',
            'zope.i18n', 'zope.i18n.interfaces', 
            'zope.i18nmessageid', 'zope.interface',
            'zope.interface.common',
            'zope.modulealias', 'zope.proxy', 'zope.schema',
            'zope.testing',]
                    
if __name__ == '__main__':
    
    setup(name='ccPublisher',
          version='1.9',
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
          py_modules=['appsetup','setup' ],
          scripts=['main.py'],
          windows=['main.py'],
          ext_modules=extensions,
          data_files=[('resources', 
                      ['resources/LICENSE.txt', 'resources/wizard.xrc'])] + 
                      findZcml(),
          packages=packages,
          options={'py2exe':{'packages':packages,
                             'includes':['dbhash', 'encodings',]
                             }
                   }
          )
