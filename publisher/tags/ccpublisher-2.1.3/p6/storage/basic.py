"""
Basic implementation of backend Storage provider.
"""

import zope.interface
import zope.component

import p6
import p6.api
import p6.extension.interfaces
import interfaces
import common

def basicStorageUi(storage):

    print 'basic', storage
    
    class BasicStorageUi(object):

        zope.interface.implements(p6.ui.interfaces.IPageList)

        def __init__(self, target, event):
            self.__pages = None
            self.__storage = storage

        def createPages(self):
            
            # XXX -- hack
            # 
            # We import here because doing so at instantiation causes problems
            # -- in particular, the App needs to be created before other
            # UI objects, and the import has side effects (querying the
            # background color)
            
            import p6.ui.pages.fieldrender
            
            # create the simple page
            fields = [
                p6.metadata.base.metadatafield(p6.metadata.types.ITextField)(
                'path', 'Destination Path')
                ]

            self.__pages = []
            
            self.__pages.append(
                lambda x: p6.ui.pages.fieldrender.SimpleFieldPage(
                x, 'BASIC_UI_META', 'Basic Storage', fields,
                self.callback))

        def list(self):
            # check if we've been activated by the interface
            
            if self.__storage.activated():
                
                if self.__pages is None:
                    self.createPages()

                return self.__pages
            else:
                # not activated, so we don't contribute to the interface
                return []

        def callback(self, value_dict):
            print value_dict

            # register for future storage events after validating our
            # storage-specific settings
            self.storage.registerEvents()

    return BasicStorageUi

class BasicStorage(common.CommonStorageMixin):
    zope.interface.implements(interfaces.IStorage)
    
    id = 'BASIC_STORAGE'
    name = 'Basic Storage'
    description = 'A simple storage provider which does nothing.'
    
    def __init__(self):

        # self.registerEvents()
        
        # register handlers for extension points --
        # this allows us to extend the user interface in a unified way
        # 
        zope.component.provideSubscriptionAdapter(
            basicStorageUi(self),
            (p6.extension.interfaces.IStorageMetaCollection,
             p6.extension.events.IExtensionPageEvent,
             ),
            p6.ui.interfaces.IPageList)

    def validate(self, event=None):
        """Handle L{p6.storage.events.IValidate} events by simply
        updating the progress bar."""
        
        update = p6.ui.events.UpdateStatusEvent(delta=20,
                                                message='validating submission data...')

        zope.component.handle(update)

    def store(self, event=None):
        """Handle L{p6.storage.events.IStore} events by simply
        updating the progress bar; fire a L{p6.storage.events.WorkStored}
        event after the "storage" process is complete.
        """
        
        update = p6.ui.events.UpdateStatusEvent(delta=20,
                                                message='in Store...')

        zope.component.handle(update)

        return {}
