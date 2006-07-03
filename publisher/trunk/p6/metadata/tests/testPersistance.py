# p6.metadata.tests.testPersistance
#
# Unittests for the P6 metdata persistance utility
#

import os
import unittest

import p6.metadata.persistance

class TestPersistance(unittest.TestCase):

    def setUp(self):
        """Create the persistance utility."""

        self.p = p6.metadata.persistance.ShelvePersistance('test.tmp')

    def tearDown(self):
        """Delete the persistance utility."""

        del self.p
        os.remove('test.tmp')
        
    def testStore(self):
        """Store a value and retrieve it, checking for equality."""

        self.p.put('group', 'key', '123')
        a = self.p.get('group', 'key')

        self.assertEqual(a, '123')
    
    def testLookup(self):
        """Attempt to retrieve a key which has not been stored; using the
        get() method should raise an error, using query should return the
        specified default."""

        self.assertRaises(KeyError, self.p.get, 'group', '123')

        self.assertEqual(self.p.query('group', 'abc'), None)

    def testPersistance(self):
        """Store a value, delete the utility and then recreate it; we should
        still be able to get to our persisted value."""

        self.p.put('group', 'key', 'gork')

        # delete the utility and recreate a new instance
        del self.p
        self.setUp()

        self.assertEqual(self.p.get('group', 'key'), 'gork')

    def testClear(self):
        """Store a value, retrieve it to make sure it's really there.  Then
        call clear; subsequent calls to get() should raise an exception."""

        self.p.put('group', 'key', 'gork')

        # delete the utility and recreate a new instance
        del self.p
        self.setUp()

        # clear the value
        self.p.clear('group', 'key')

        # delete the utility and recreate a new instance
        del self.p
        self.setUp()

        # attempt to retrieve our old value
        self.assertEqual( self.p.query('group', 'key'), None )
        
if __name__ == '__main__':
    unittest.main()
    
