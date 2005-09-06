"""Storage event interfaces and declarations."""

import zope.interface
import zope.component as component

class IValidate(zope.interface.Interface):
    """Validation event interface; validation errors are collected in
    the errors attribute.
    """
    
    errors = zope.interface.Attribute("A sequence of error messages.")

class ValidateWork:
    """Validation Event"""
    
    zope.interface.implements(IValidate)
    def __init__(self):
        self.errors = []
        
class IStore(zope.interface.Interface):
    """Placeholder interface for StoreWork events."""

class StoreWork:
    zope.interface.implements(IStore)
    def __init__(self):
        pass
    
class IStored(zope.interface.Interface):
    """Placeholder interface for post-Storage (WorkedStored) events."""

    metadata = zope.interface.Attribute("A dictionary of metadata returned by the storage provider.")

class WorkStored:
    zope.interface.implements(IStored)
    def __init__(self, metadata = {}):
        self.metadata = metadata
    
class IItemSelected(zope.interface.Interface):
    """Interface for item selection events."""
    
    item = zope.interface.Attribute("The item selected; "
                                    "item should implement "
                                    "p6.storage.interfaces.IWorkItem")

class ItemSelected:
    """Event fired when an item is selected to notify other application
    components of the change."""
    
    zope.interface.implements(IItemSelected)
    
    def __init__(self, item):
        """
        @param item: The newly select Item object
        @type  item: implements L{p6.storage.interfaces.IWorkItem}.
        """
        self.item = item
    
class IItemDeselected(zope.interface.Interface):
    """Interface for item de-selection events."""
    
    item = zope.interface.Attribute("The item deselected.")

class ItemDeselected:
    """Event fired when an item is deselected to notify other application
    components of the change."""
    
    zope.interface.implements(IItemDeselected)
    
    def __init__(self, item):
        """
        @param item: The newly deselect Item object
        @type  item: implements L{p6.storage.interfaces.IWorkItem}.
        """
        
        self.item = item
        
