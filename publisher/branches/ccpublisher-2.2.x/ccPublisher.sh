#!/bin/sh

# ccPublisher 2 Runtime script
# Correctly sets the Python path information so that String encodings
# work correctly.
#
# (c) 2006, Creative Commons, Nathan R. Yergler
# Licensed to the public under the GNU GPL version 2.
# see resources/LICENSE.txt for details

PYTHONPATH=.:$PYTHONPATH python ccp.py
