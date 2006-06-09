import zope.interface

class IActivated(zope.interface.Interface):
    """ XXX """

class IDeactivated(zope.interface.Interface):
    """ XXX """

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
