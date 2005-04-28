import zope.interface

class ICollectGroups(zope.interface.Interface):
    itemType = zope.interface.Attribute("")

    def addGroup(newGroup):
        """Add the new group to the collection."""
        
    def getGroups():
        """Returns a list of the metadata groups being provided."""
        
class CollectGroups:
    zope.interface.implements(ICollectGroups)

    def __init__(self, itemInterface):
        self.itemType = itemInterface
        self.groups = []
        
    def addGroup(self, group):
        self.groups.append(group)
        
    def getGroups(self):
        return self.groups
    
    
