import zope.interface

class IExtensionPoint(zope.interface.Interface):
    """ XXX """

    def call():
        """ XXX """

        
class IStorageMetaCollection(zope.interface.Interface):
    pass

class IPostStoreExtension(zope.interface.Interface):
    pass

class IStorageProcessing(zope.interface.Interface):
    pass
