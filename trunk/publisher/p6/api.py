import wx
import zope.interface
import p6

def deinstify(func):
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
    return wx.GetApp()


def findField(field_id, item=None):

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
