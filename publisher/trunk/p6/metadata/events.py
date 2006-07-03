"""
Interfaces and classes for metadata events.
"""

import p6
import zope.interface

class IUpdateMetadataEvent(zope.interface.Interface):
    """Placeholder interface for metadata update events."""
    
    item = zope.interface.Attribute(
        "The item or interface the field applies to.")

    #group = zope.interface.Attribute(
    #    "The metadata group this field belongs to.")
    
    field = zope.interface.Attribute("The metadata field being updated.")
    canonical = zope.interface.Attribute("The canonical URI of the field being updated.")
    
    value = zope.interface.Attribute("The new value of the metadata field.")

class UpdateMetadataEvent(object):
    """An event for updating the metadata value for a field that applies to
    a particular item.
    """
    
    zope.interface.implements(IUpdateMetadataEvent)

    def __init__(self, item, field_or_canonical, value):
        """
        @param item: The item we're updating metadata for
        @param field_or_canonical: The metadata field we're updating -- either a field object or a string with the canonical URI for a field
        @param value: The new value for this field
        """
        
        # XXX Raising error here to find problem cases
        if item is None:
            raise Exception("item==None no longer permitted.")
            
        self.item = item

        if isinstance(field_or_canonical, str):
            self.field = p6.api.fieldFromCanonical(field_or_canonical)
            self.canonical = field_or_canonical
        else:
            self.field = field_or_canonical
            self.canonical = self.field.canonical
            
        self.value = value
