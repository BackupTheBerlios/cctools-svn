"""
Application Extension API
"""

import os
import sys
import fnmatch
import platform

import zope
import p6.api

class ExtensionPrefField(object):
    def __init__(self, id, type, label, value=None):
        self.id = id
        self.type = type
        self.label = label

        self.value = value
        
class ExtensionPrefs(object):
    def __init__(self, id, label, fields={}):
        self.id = id
        self.label = label

        self.fields = fields
    
def extPaths():
    """Return a list of paths to search for extensions and plugins."""

    return [os.path.join(os.path.abspath('.'), 'extensions'),
            os.path.join(p6.api.getSupportDir(), 'extensions')
            ]

def extConfs(path):
    """Generates a list of configuration files in the specified path;
    searches path and all subfolders for 'extension.zcml'."""
    
    for (path, dirnames, filenames) in os.walk(path):
        for f in fnmatch.filter(filenames, 'extension.zcml'):
            yield os.path.join(path, f)

def loadExtension(extzcml, context):
    """Loads the extension specified by [extzcml] -- modifies the Python
    Path to include the folder containing [extzcml]."""

    sys.path.insert(0, os.path.dirname(extzcml))
    zope.configuration.xmlconfig.file(extzcml, context=context)
