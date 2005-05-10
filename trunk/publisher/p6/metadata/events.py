import zope.interface


class IUpdateMetadataEvent(zope.interface.Interface):
    item = zope.interface.Attribute("")
    
    key = zope.interface.Attribute("")
    value = zope.interface.Attribute("")

class UpdateMetadataEvent(object):
    zope.interface.implements(IUpdateMetadataEvent)

    def __init__(self, item, key, value):
        # XXX Raising error here to find problem cases
        if item is None:
            raise Exception("item==None no longer permitted.")
            
        self.item = item
        self.key = key
        self.value = value
        
