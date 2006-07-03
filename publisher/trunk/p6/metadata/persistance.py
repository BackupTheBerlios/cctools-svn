"""Basic metadata persistance functionality.

XXX Note this implementation does not support storing metadata
values which may apply to multiple objects or interfaces with
multiple implementors.
"""

import os
import shelve

import zope.interface

import p6

try:
    PERST_FILE = os.path.join(p6.api.getSupportDir(), 'p6.settings')
except:
    PERST_FILE = 'p6.settings'

class IMetadataPersistance(zope.interface.Interface):
    """Utility implementing metadata persistance."""

    def put(group, key, value):
        """Store the value for the group:key combination."""

    def get(group, key):
        """Retrieve the persisted value of the group:key combination; if
        not found, raises a KeyError."""

    def query(group, key, default=None):
        """Attempt to retrieve the persisted value for the group:key; if
        not found, return the specified default value (or None if no default
        specified."""

    def clear(group, key):
        """Clear the group:key from the persistant store; if group:key
        is not found, do not raise an exception."""
        
class ShelvePersistance(object):
    """Simple shelve-based persistance model. """
    zope.interface.implements(IMetadataPersistance)

    def __init__(self, filename=PERST_FILE):

        self.__filename = filename

    def __openFile(self):
        """Open the persistant shelf and return the handle to it."""

        return shelve.open(self.__filename, writeback=True)
        
    def put(self, group, key, value):
        """Stores a metadata value to persistant storage.

        @param group: The metadata group ID this field belongs to.
        @type group: String
        @param key: The metadata field ID to be stored.
        @type key: String
        @param value: The value to store.
        """

        p_store = self.__openFile()

        g_dict = p_store.get(group, {})
        g_dict[key] = value

        p_store[group] = g_dict

        p_store.close()

    def get(self, group, key):
        """Load a metadata value from persistant storage.

        @param group: The metadata group ID this field belongs to.
        @type  group: String
        @param key: The metadata field ID to be loaded.
        @type  key: String

        @raise KeyError: If the group-key combination is not found in storage.
        """

        p_store = self.__openFile()
        result = p_store[group][key]

        p_store.close()

        return result

    def query(self, group, key, default=None):

        try:
            return self.get(group, key)
        except KeyError, e:
            return default
    
    def clear(self, group, key):
        """Clear the group:key from the persistant store; if group:key
        is not found, do not raise an exception."""

        p_store = self.__openFile()

        if group in p_store:
            if key in p_store[group]:
                del p_store[group][key]

        p_store.close()
        
