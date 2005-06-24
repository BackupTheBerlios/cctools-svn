"""Implementation of Item and Work objects."""

import zope.interface
import interfaces

import p6
from p6.metadata.base import BasicMetadataStorage

class Item(BasicMetadataStorage):
    """Basic item class which all Works and Items sub-class."""
    zope.interface.implements(interfaces.IItem)

class RootItem(Item):
    """A top-level work; this implementation enforces singularity."""
    
    zope.interface.implements(interfaces.IWork)

    def getIdentifier(self):
        """Return the identifier, 'ROOT'."""
        return "ROOT"

class FileItem(Item):
    """A file-based item belonging to a Work."""
    
    zope.interface.implements(interfaces.IWorkItem, interfaces.IFileItem)
    
    def __init__(self, filename):
        """
        @param filename: the filename of the file containing the data for
           this item
        @type filename: String
        """
        
        super(self.__class__, self).__init__()
        
        self.filename = filename

    def getIdentifier(self):
        """Return the identifier, in this case the filename."""
        return self.filename
    
class FileItemStream:
    """An adapter from an object implementing
    L{p6.storage.interfaces.IFileItem} to
    L{p6.storage.interfaces.IInputStream}.
    """
    
    zope.interface.implements(interfaces.IInputStream)
    
    def __init__(self, fileitem):
        """
        @param fileitem: the object to adapt to IInputStream.
        @type fileitem: implements L{p6.storage.interfaces.IInputStream}
        """
        self.__item = fileitem
        self.__fname = fileitem.getIdentifier()

    def __call__(self):
        """Return an open file handle."""
        return file(self.__fname)
    
    
