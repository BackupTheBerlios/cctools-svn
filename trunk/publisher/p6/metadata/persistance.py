"""Basic metadata persistance functionality.

XXX Note this implementation does not support storing metadata
values which may apply to multiple objects or interfaces with
multiple implementors.
"""

import os
import shelve

import p6

PERST_FILE = 'p6.settings'

def item_id(item):
    """Returns a callable which can be used to get the identifier for a class;
    if the item has a getIdentifier method, we use that.

    @rtype: callable
    """
    
    return getattr(item, 'getIdentifier',
                         lambda : item.__class__)()

    
def store(group, key, value):
    """Stores a metadata value to persistant storage.

    @param group: The metadata group ID this field belongs to.
    @type group: String
    @param key: The metadata field ID to be stored.
    @type key: String
    @param value: The value to store.
    """

    print 'persisting %s:%s (%s) ...' % (group, key, value)
    
    p_store = shelve.open(os.path.join(p6.api.getAppSupportDir(),
                                       PERST_FILE))

    g_dict = p_store.get(group, {})
    g_dict[key] = value

    p_store[group] = g_dict

    p_store.close()
    
def get(group, key):
    """Load a metadata value from persistant storage.

    @param group: The metadata group ID this field belongs to.
    @ptype group: String
    @param key: The metadata field ID to be loaded.
    @type key: String

    @raise KeyError: If the group-key combination is not found in storage.
    """

    print 'loading %s:%s ...' % (group, key)

    p_store = shelve.open(os.path.join(p6.api.getAppSupportDir(),
                                       PERST_FILE))

    result = p_store[group][key]
    print 'the result is ... ', result
    
    p_store.close()

    return result

    
