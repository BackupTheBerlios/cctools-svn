import os
from distutils.core import Extension

# Packages to include
packages = ['ccpublisher', 'ccpublisher.ui',
            'p6', 'p6.app', 'p6.app.support',
            'p6.configure', 'p6.zcmlsupport',
            'p6.metadata', 
            'p6.storage','p6.storage.providers',
            'p6.ui', 'p6.ui.pages', 'p6.ui.windows',
            'p6.extension',
            'pyarchive', 'ccrdf', 'tagger', 'ccwsclient',
            'ccwx','eyeD3',
            'cctagutils', 'cctagutils.filetypes',
            'libfeedback',
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
            'zope.i18nmessageid', 'zope.interface',
            'zope.interface.common', 'zope.schema',
            'zope.testing',]

classifiers = ['Development Status :: 5 - Production/Stable',
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
        ]
desc = "Desktop tools for licensing works and uploading to the Internet Archive for hosting and cataloging."

long_desc = ""
