"""
p6.api

Collects frequently used functions in a single module.
"""

import wx
import zope.interface
import p6

def deinstify(func):
    """Decorator to strip an instance method of it's "self" paramter,
    making it work properly as a non-bound function or adapter.

    @param func: The instance method to decorate
    @type func: Bound instance method (callable)

    @rtype: Unbound callable
    """
    
    def foo(*args, **kwargs):
        func(*args, **kwargs)
        
    return foo

def nearest(items, target):
    if len(items) == 1:
        return items[0]

    for n in items:
        print zope.interface.implementedBy(n.__class__)

    return items[-1]

def getApp():
    """Returns a reference to the current Application object.

    @return: the current Application object
    @rtype: wx.App
    """
    return wx.GetApp()

def group(groupid):
    """Convenience function for finding a metadata group by id."""

    return [n for n in p6.api.getApp().groups if
            n.id == groupid][0]

def fieldFromCanonical(canonical):
    """Returns the field object with the canonical uri specified."""
    for g in p6.api.getApp().groups:
        for f in g.fields:
            if f.canonical == canonical:
                return f


    return None

def findField(field_id, item=None):
    """Returns the value of the metadata field specified.

    @param field_id: the identifier of the field to retrieve
    @type field_id: string
    @param item: the item we want the value to apply to, or None for Work
    @type item: None or adaptable to p6.metadata.interfaces.IMetadataStorage

    @return: the value of the metadata field
    """
    
    if item is None:
        # This applies to any root item
        for i in p6.api.getApp().items:
            if p6.storage.interfaces.IWork in \
                   zope.interface.implementedBy(i.__class__):
                result = p6.metadata.interfaces.IMetadataStorage(i).getMetaValue(
                    field_id)
                
    else:
        result = p6.metadata.interfaces.IMetadataStorage(item).getMetaValue(field_id)

    return result

def getAppSupportDir():
    """Returns the Application Support directory where we can store
    preferences and persisted metadata information.


    @return: path to the application directory
    @rtype: string
    """

    # XXX
    return getApp().resource_dir # '.'

def updatePref(setid, fieldid, value):
    getApp().prefs[setid].fields[fieldid].value = value

def workInformation():

    # collect the work information
    return {'title'       : findField('title'),
            'type'        : findField('format'),
            'year'        : findField('year'),
            'description' : findField('description'),
            'holder'      : findField('holder'),
            }
    
