import zope.interface


class IStorageRegistry(zope.interface.Interface):
    """Interface for the storage provider registry."""

    def register(id, name, factory, description=''):
        """Register a new storage provider identified by [name]; [factory]
        specifies a callable which will create an instance of the provider."""

    def identifiers():
        """Return a sequence of provider identifiers."""

    def __getitem__(self, id):
        """Return the registry item associated with the specified id."""

class IStorageRegistryItem(zope.interface.Interface):
    """Interface for an item stored in the provider registry."""

    id = zope.interface.Attribute("The unique identifier for this provider.""")
    name = zope.interface.Attribute(
        "The message id for the human readable name of this provider.")
    description = zope.interface.Attribute(
        "The message id for the human readable description.")

    instance = zope.interface.Attribute(
        "The instance of the storage provider, if activated.")

    def activate():
        """Activate the storage provider, if not already activated."""

    def deactivate():
        """Deactivate the storage provider if previously activated."""

    def isActivated():
        """Return True if activated, False if not."""
        
class StorageRegistryItem(object):
    """Simple storage provider registry item which collects the
    relevant information."""

    zope.interface.implements(IStorageRegistryItem)
    
    def __init__(self, id, name, factory, description=''):

        self.id = id
        self.name = name
        self.factory = factory
        self.description = description

        self.instance = None
        
    def activate(self):
        """Activate the storage provider, if not already activated."""

        if self.instance is None:
            self.instance = self.factory()

    def deactivate(self):
        """Deactivate the storage provider if previously activated."""


        if self.instance is not None:
            del self.instance
            self.instance = None

    def isActivated(self):
        """Return True if activated, False if not."""

        return (self.instance is not None)
        
    
class StorageRegistry(object):
    """Basic storage registry implementation."""

    zope.interface.implements(IStorageRegistry)

    def __init__(self):
        """Initialize the registry."""
        
        self.__providers = {}
        self.__ids = []
        
    def register(self, id, name, factory, description=''):
        """Register a new storage provider identified by [name]; [factory]
        specifies a callable which will create an instance of the provider."""

        self.__providers[id] = StorageRegistryItem(
            id, name, factory, description)
        self.__ids.append(id)

    def identifiers(self):
        """Return a sequence of provider identifiers."""

        return [n for n in self.__ids]

    def __getitem__(self, id):
        """Return the storage registry item specified by the identifier."""

        return self.__providers[id]
