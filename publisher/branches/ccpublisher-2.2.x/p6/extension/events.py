import zope.interface

class IExtensionPageEvent(zope.interface.Interface):
    pass

class ExtensionPageEvent(object):
    zope.interface.implements(IExtensionPageEvent)

    def __init__(self):

        self.__pageSets = []

    def addPageSet(self, pageSet):
        if pageSet:
            self.__pageSets.append(pageSet)

    def getPageSets(self):
        return self.__pageSets
