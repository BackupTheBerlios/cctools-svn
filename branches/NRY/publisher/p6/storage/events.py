import zope.interface
import zope.component as component

class IValidate(zope.interface.Interface):
    errors = zope.interface.Attribute("A sequence of error messages.")

class ValidateWork:
    zope.interface.implements(IValidate)
    def __init__(self):
        self.errors = []
        
class IStore(zope.interface.Interface):
    pass

class StoreWork:
    zope.interface.implements(IStore)
    def __init__(self):
        pass
    
class IStored(zope.interface.Interface):
    pass

class WorkStored:
    zope.interface.implements(IStored)
    def __init__(self):
        pass
    
class IItemSelected(zope.interface.Interface):
    item = zope.interface.Attribute("The item selected; "
                                    "item should implement "
                                    "p6.storage.interfaces.IWorkItem")

class ItemSelected:
    zope.interface.implements(IItemSelected)
    def __init__(self, item):
        self.item = item
    
class IItemDeselected(zope.interface.Interface):
    item = zope.interface.Attribute("The item deselected.")

class ItemDeselected:
    zope.interface.implements(IItemDeselected)
    def __init__(self, item):
        self.item = item
        
