"""
Application Extension API
"""

import os
import sys
import fnmatch
import platform

import zope

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
    PLATFORM = platform.system().lower()

    if PLATFORM == 'windows':
        # load paths from registry

        import _winreg
        import win32con

        # Find the P6 path
        KEY_PATH = [win32con.HKEY_LOCAL_MACHINE, 'SOFTWARE', 'P6', ]
        p6key = KEY_PATH[0]
        for k in KEY_PATH[1:]:
            p6key = _winreg.OpenKey(p6key, k)

        P6_SHARE_PATH = _winreg.QueryValueEx(p6key, 'SharedPath')[0]

        p6_ext_path = os.path.join(P6_SHARE_PATH, 'extensions')
        if os.path.exists(p6_ext_path):
            results.append(p6_ext_path)

    elif PLATFORM == 'linux':
        # always look in the current working directory
        # XXX Should this go away? It's sorta needed for dev work
        result = ['.']
        
        # check if the autopackage non-root share exists
        ap_local_path = os.path.join(os.path.expanduser('~'),
                                     '.local', 'share',
                                     'p6', 'extensions')
        if os.path.exists(ap_local_path):
            result.append(ap_local_path)

        # check for the global autopackage share
        ap_root_path = os.path.join('/', 'usr', 'local', 'share', 'p6',
                                    'extensions')
        if os.path.exists(ap_root_path):
            result.append(ap_root_path)

        return result
    
    elif PLATFORM == 'darwin':
        pass
    else:
        return []

def extConfs(path):
    """Generates a list of configuration files in the specified path;
    searches path and all subfolders for 'extension.zcml'."""
    
    for (path, dirnames, filenames) in os.walk('.'):
        for f in fnmatch.filter(filenames, 'extension.zcml'):
            yield os.path.join(path, f)

def loadExtension(extzcml, context):
    """Loads the extension specified by [extzcml] -- modifies the Python
    Path to include the folder containing [extzcml]."""

    sys.path.insert(0, os.path.dirname(extzcml))
    zope.configuration.xmlconfig.file(extzcml, context=context)
