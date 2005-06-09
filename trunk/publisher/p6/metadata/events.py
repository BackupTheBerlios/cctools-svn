import zope.interface

class IUpdateMetadataEvent(zope.interface.Interface):
    item = zope.interface.Attribute(
        "The item or interface the field applies to.")

    group = zope.interface.Attribute(
        "The metadata group this field belongs to.")
    field = zope.interface.Attribute("The metadata field being updated.")
    
    value = zope.interface.Attribute("The new value of the metadata field.")

class UpdateMetadataEvent(object):
    zope.interface.implements(IUpdateMetadataEvent)

    def __init__(self, item, group, field, value):
        
        # XXX Raising error here to find problem cases
        if item is None:
            raise Exception("item==None no longer permitted.")
            
        self.item = item

        self.group = group
        self.field = field

        self.value = value
        
class ILoadMetadataEvent(zope.interface.Interface):
    item = zope.interface.Attribute(
        "The item or interface the field applies to.")

    group = zope.interface.Attribute(
        "The metadata group this field belongs to.")
    field = zope.interface.Attribute("The metadata field being updated.")
    
    value = zope.interface.Attribute("The new value of the metadata field.")

class LoadMetadataEvent(object):
    zope.interface.implements(ILoadMetadataEvent)

    def __init__(self, item, group, field):
        
        # XXX Raising error here to find problem cases
        if item is None:
            raise Exception("item==None no longer permitted.")
            
        self.item = item

        self.group = group
        self.field = field

        self.value = []
