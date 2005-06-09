import zope.interface
import interfaces

import p6
from p6.metadata.base import BasicMetadataStorage

class Item(BasicMetadataStorage):
    zope.interface.implements(interfaces.IItem)

class RootItem(Item):
    zope.interface.implements(interfaces.IWork)

    def getIdentifier(self):
        return "ROOT"

class FileItem(Item):
    zope.interface.implements(interfaces.IWorkItem, interfaces.IFileItem)
    def __init__(self, filename):
        super(self.__class__, self).__init__()
        
        self.filename = filename

    def getIdentifier(self):
        return self.filename
    
class FileItemStream:
    zope.interface.implements(interfaces.IInputStream)
    def __init__(self, fileitem):
        #super(self.__class__, self).__init__()
        self.__item = fileitem
        self.__fname = fileitem.getIdentifier()

    def __call__(self):
        return file(self.__fname)
    
    
