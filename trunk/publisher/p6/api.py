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
        print
        print 'event.item is None'
        print 'event.key is ', field_id
        
        # no item discriminator; just find the first default mention of this
        # field name
        for g in p6.api.getApp().groups:
            for f in g.getFields():
                print 'checking ', f.id
                if f.id == field_id:
                    return f()
    else:
        # find the metadata for this type of item and work from there
        for g in p6.api.getApp().groups:
            meta_dicts = [n[1] for n in
                         zope.component.getGlobalSiteManager().getAdapters(
               (g, item),
               p6.metadata.interfaces.IMetadataDict)
                         if n]

            for m in meta_dicts:
                if field_id in m:
                    return m[field_id]

    return None

    print event
    print event.key, event.item
