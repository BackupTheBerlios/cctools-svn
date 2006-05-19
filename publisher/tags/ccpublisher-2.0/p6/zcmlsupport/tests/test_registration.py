##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Registration Tests

$Id$
"""
__docformat__ = "reStructuredText"
import unittest

import zope.component.testing as placelesssetup
from zope.testing import doctest
from zope.app.testing import setup

def setUp(test):
    placelesssetup.setUp(test)
    setup.setUpAnnotations()
    setup.setUpDependable()
    setup.setUpTraversal()

def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite('../statusproperty.txt'),
        doctest.DocFileSuite('../registration.txt',
                             setUp=setUp, tearDown=placelesssetup.tearDown),
        ))

if __name__ == "__main__":
    unittest.main(defaultTest='test_suite')
