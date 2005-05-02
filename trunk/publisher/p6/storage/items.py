import zope.interface
import interfaces

class RootItem:
    zope.interface.implements(interfaces.IWork)

    def getIdentifier(self):
        return "ROOT"

class FileItem:
    zope.interface.implements(interfaces.IWorkItem)
    def __init__(self, filename):
        self.filename = filename

    def getIdentifier(self):
        return self.filename
    
