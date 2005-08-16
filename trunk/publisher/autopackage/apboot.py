#!/usr/bin/env python

"""Semi-generic Autopackge Bootstrap Script

Sets up the Python path to point at $PREFIX/share/site-packages, and then
runs the function specified on the commandline, passing it the
remainder of sys.argv.  For example,

$ apboot.py publisher.main.main

will attempt to do the following (roughly):

from publisher.main import main
main(sys.argv)
"""

import sys
import os
import imp

SHARE_PATH = os.path.normpath(os.path.join(os.path.split(__file__)[0],
                          '..',
                          'share',
                          'site-packages'
                          ))

sys.path.insert(0, SHARE_PATH)

import main
main.main(sys.argv)

