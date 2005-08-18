#!/usr/bin/env python

"""
Semi-generic Autopackage Bootstrap Script

Sets up the Python path to point at $PREFIX/share/site-packages, and then
imports the module specified on the commandline and looks for a callable
named 'main' which is called with the remainder of sys.argv.  For example,

$ apboot.py publisher.main

will attempt to do the following (roughly):

import publisher.main as app
app.main(sys.argv)

"""

APPNAME = 'ccPublisher'
import sys
import os
import platform

PLATFORM = platform.system().lower()

# include additional dependencies that are really P6 dependencies
# this is sort of ugly, but works
try:
    import wx
    import wx.xrc
    import weakref
    import shelve
    import logging
    import sets
    import encodings
    import keyword
    import __future__
except Exception, e:
    if PLATFORM == 'windows':
        raise e
    else:
        pass

if PLATFORM == 'linux':

    # Add the P6 path to the PYTHONPATH
    SHARE_PATH = os.path.abspath(
        os.path.normpath(
        os.path.join(os.path.dirname(__file__),
                              '..',
                              'share',
                              'p6', 'site-packages',
                              )))
    sys.path.insert(0, SHARE_PATH)

    # Add the application path to the PYTHONPATH
    SHARE_PATH = os.path.abspath(
        os.path.normpath(
        os.path.join(os.path.dirname(__file__),
                              '..',
                              'share', APPNAME, 'site-packages',
                              )))
    
    sys.path.insert(0, SHARE_PATH)
elif PLATFORM in ('windows', 'win32', 'win'):
    print 'fixing path for Windows...'
    import win32con
    import _winreg

    # Add the P6 path to the PYTHONPATH
    KEY_PATH = [win32con.HKEY_LOCAL_MACHINE, 'SOFTWARE', 'P6', ]
    p6key = KEY_PATH[0]
    for k in KEY_PATH[1:]:
        p6key = _winreg.OpenKey(p6key, k)

    P6_SHARE_PATH = _winreg.QueryValueEx(p6key, 'SharedPath')[0]
    sys.path.insert(0, P6_SHARE_PATH)

    # Add the application path to the PYTHONPATH
    KEY_PATH = [win32con.HKEY_LOCAL_MACHINE, 'SOFTWARE', APPNAME, ]
    p6key = KEY_PATH[0]
    for k in KEY_PATH[1:]:
        p6key = _winreg.OpenKey(p6key, k)

    P6_SHARE_PATH = _winreg.QueryValueEx(p6key, 'Path')[0]
    sys.path.insert(0, os.path.join(P6_SHARE_PATH, 'site-packages'))

elif PLATFORM == 'darwin':
    pass
else:
    pass

print sys.path

main = sys.argv[1]
argv = sys.argv[:1] + sys.argv[2:]

statements = """
import p6
import %s as main

""" % main
bootstrap = compile(statements, '<bootstrap>', 'exec')
exec(bootstrap)

main.main(argv)

