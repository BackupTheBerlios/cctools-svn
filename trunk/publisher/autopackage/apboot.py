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

APPNAME = 'ccpublisher'

import sys
import os
import platform

PLATFORM = platform.system().lower()

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

main = sys.argv[1]
argv = sys.argv[:1] + sys.argv[2:]

statements = """
import p6
import %s as main

""" % main
bootstrap = compile(statements, '<bootstrap>', 'exec')
exec(bootstrap)

main.main(argv)

