import zope.interface
import interfaces

class FileItem:
    zope.interface.implements(interfaces.IWorkItem)
    def __init__(self, filename):
        self.filename = filename

    def getIdentifier(self):
        return self.filename
    
