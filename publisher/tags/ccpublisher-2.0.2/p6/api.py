"""
p6.api

Collects frequently used functions in a single module.
"""

import platform
import os.path

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

def getResourceDir():
    """Returns the Application Resource directory where user interface
    definitions, version information and images are stored.


    @return: path to the application resource directory
    @rtype: string
    """

    return getApp().resource_dir

def getSupportDir():
    """Returns the Application Support directory where user settings
    and extensions are stored.

    @return: path to the application support directory
    @rtype: string
    """

    PLATFORM = platform.system().lower()
    user_home = os.path.expanduser('~')
    
    if (PLATFORM == 'windows'):
        return os.path.join(user_home, 'Application Data', 'ccPublisher')

    elif (PLATFORM == 'darwin'):
        return os.path.join(user_home, 'Library', 'Application Support',
                            'ccPublisher')
    elif (PLATFORM == 'linux'):
        return os.path.join(user_home, '.ccpublisher')

    else:
        return '.'

def checkAppDirs():
    """Ensure that the resource and support directories exist;
    if resources does not exist, raise an exception.  If support and
    support/extensions does not exist, create them."""

    if not(os.path.exists(getResourceDir())):
        # resource dir *must* be there
        raise Exception()

    if not(os.path.exists(getSupportDir())):
        os.makedirs(getSupportDir())

    if not(os.path.exists(os.path.join(getSupportDir(), 'extensions'))):
        os.makedirs(os.path.join(getSupportDir(), 'extensions'))
        
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
    
