"""
Basic implementation of backend Storage provider.
"""

import zope.interface
import zope.component

import p6
import p6.api
import p6.extension.interfaces
import interfaces

def basicStorageUi(storage):
    
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
            if self.__pages is None:
                self.createPages()
                
            return self.__pages

        def callback(self, value_dict):
            print value_dict
            pass

    return BasicStorageUi

class BasicStorage(object):
    zope.interface.implements(interfaces.IStorage)
    
    id = 'BASIC_STORAGE'
    name = 'Basic Storage'
    description = 'A simple storage provider which does nothing.'
    
    def __init__(self):
        
        zope.component.provideHandler(
            zope.component.adapter(p6.storage.events.IValidate)(
                p6.api.deinstify(self.validate))
            )

        zope.component.provideHandler(
            zope.component.adapter(p6.storage.events.IStore)(
                p6.api.deinstify(self.__wrapStore))
            )

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

    def __wrapStore(self, event=None):
        """Wraps dispatch of L{p6.storage.events.IStore} events by calling
        self.store(self, event).  Publishes a L{p6.storage.events.WorkStored}
        event after .store completes.
        """

        update = p6.ui.events.UpdateStatusEvent(delta=20,
                                                message='uploading submission...')

        zope.component.handle(update)

        # call the store method
        mdata = self.store(event)
        
        # after the storage process, publish a post-store event
        stored_event = p6.storage.events.WorkStored(mdata)
        zope.component.handle(stored_event)

    def store(self, event=None):
        """Handle L{p6.storage.events.IStore} events by simply
        updating the progress bar; fire a L{p6.storage.events.WorkStored}
        event after the "storage" process is complete.
        """
        
        update = p6.ui.events.UpdateStatusEvent(delta=20,
                                                message='in Store...')

        zope.component.handle(update)

        return {}
