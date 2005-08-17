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

import sys
import os

SHARE_PATH = os.path.abspath(
    os.path.normpath(
    os.path.join(os.path.dirname(__file__),
                          '..',
                          'share',
                          'site-packages'
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

