import zope.interface

class IItem(zope.interface.Interface):
    pass

class IWork(IItem):
    pass

class IWorkItem(IItem):
    def getIdentifier():
        """Returns the unique identifier (filename, etc) for this item."""

class IStorage(zope.interface.Interface):

    def validate():
        """Walks through the item and metadata models, ensuring everything
        needed for the storing process is in place."""

    def store():
        """Perform the storage process."""
