#!/usr/bin/env python

"""P6 bootstrap script for use with autopackage installations."""

import sys
import os

SHARE_PATH = os.path.normpath(os.path.join(os.path.split(__file__)[0],
                          '..',
                          'share',
                          'ccpublisher'
                          ))

sys.path.insert(0, SHARE_PATH)
import main
main.main(sys.argv)

