import zope.interface


class IUpdateMetadataEvent(zope.interface.Interface):
    item = zope.interface.Attribute("")
    
    key = zope.interface.Attribute("")
    value = zope.interface.Attribute("")

class UpdateMetadataEvent(object):
    zope.interface.implements(IUpdateMetadataEvent)

    def __init__(self, item, key, value):
        self.item = item
        self.key = key
        self.value = value
        
