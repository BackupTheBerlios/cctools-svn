"""
Interfaces and classes for metadata events.
"""

import zope.interface

class IUpdateMetadataEvent(zope.interface.Interface):
    """Placeholder interface for metadata update events."""
    
    item = zope.interface.Attribute(
        "The item or interface the field applies to.")

    group = zope.interface.Attribute(
        "The metadata group this field belongs to.")
    field = zope.interface.Attribute("The metadata field being updated.")
    
    value = zope.interface.Attribute("The new value of the metadata field.")

class UpdateMetadataEvent(object):
    """An event for updating the metadata value for a field that applies to
    a particular item.
    """
    
    zope.interface.implements(IUpdateMetadataEvent)

    def __init__(self, item, group, field, value):
        """
        @param item: The item we're updating metadata for
        @param group: The metadata group this field belongs to
        @param field: The metadata field we're updating
        @param value: The new value for this field
        """
        
        # XXX Raising error here to find problem cases
        if item is None:
            raise Exception("item==None no longer permitted.")
            
        self.item = item

        self.group = group
        self.field = field

        self.value = value
        
class ILoadMetadataEvent(zope.interface.Interface):
    """Placeholder interface for LoadMetadata events; LoadMetadata events
    are used to retrieve metadata values from persistant storage."""
    
    item = zope.interface.Attribute(
        "The item or interface the field applies to.")

    group = zope.interface.Attribute(
        "The metadata group this field belongs to.")
    field = zope.interface.Attribute("The metadata field being updated.")
    
    value = zope.interface.Attribute("The new value of the metadata field.")

class LoadMetadataEvent(object):
    zope.interface.implements(ILoadMetadataEvent)

    def __init__(self, item, group, field):
        """
        @param item: The item we're retrieving metadata for
        @param group: The metadata group this field belongs to
        @param field: The metadata field we're looking for
        """
        
        # XXX Raising error here to find problem cases
        if item is None:
            raise Exception("item==None no longer permitted.")
            
        self.item = item

        self.group = group
        self.field = field

        self.value = []
