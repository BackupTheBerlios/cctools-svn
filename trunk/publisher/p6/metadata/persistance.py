import os
import shelve

import p6

PERST_FILE = 'p6.settings'

def item_id(item):
    
    return getattr(item, 'getIdentifier',
                         lambda : item.__class__)()

    
def store(group, key, value):

    print 'persisting %s:%s (%s) ...' % (group, key, value)
    
    p_store = shelve.open(os.path.join(p6.api.getAppSupportDir(),
                                       PERST_FILE))

    g_dict = p_store.get(group, {})
    g_dict[key] = value

    p_store[group] = g_dict

    p_store.close()
    
def get(group, key):

    print 'loading %s:%s ...' % (group, key)

    p_store = shelve.open(os.path.join(p6.api.getAppSupportDir(),
                                       PERST_FILE))

    result = p_store[group][key]
    print 'the result is ... ', result
    
    p_store.close()

    return result

    
