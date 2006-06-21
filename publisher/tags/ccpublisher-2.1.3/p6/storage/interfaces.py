"""Storage interfaces"""

import zope.interface

class IItem(zope.interface.Interface):
    """Basic item interface; works and actual Items all implement this."""
    
    def getIdentifier():
        """Returns the unique identifier (filename, etc) for this item."""

class IWork(IItem):
    """Placeholder interface for root-level Work objecst."""

class IWorkItem(IItem):
    """Placeholder interface for items which are part of a larger Work."""

class IFileItem(IWorkItem):
    """Placeholder interface for file-based items which are part of a Work."""

class IStorage(zope.interface.Interface):
    """Interface for backend storage providers."""

    id = zope.interface.Attribute("The unique identifier for this provider.")
    name = zope.interface.Attribute("The human readable name for this provider.")
    description = zope.interface.Attribute("A description")
    
    def validate():
        """Walks through the item and metadata models, ensuring everything
        needed for the storing process is in place."""

    def store():
        """Perform the storage process."""


class IInputStream(zope.interface.Interface):
    """An interface representing a Python file-like object."""
    
