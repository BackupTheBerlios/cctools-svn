"""
Basic implementation of backend Storage provider.
"""

import zope.interface
import zope.component

import p6
import p6.api
import interfaces

class BasicStorage(object):
    zope.interface.implements(interfaces.IStorage)

    def __init__(self):
        
        zope.component.provideHandler(
            zope.component.adapter(p6.storage.events.IValidate)(
                p6.api.deinstify(self.validate))
            )

        zope.component.provideHandler(
            zope.component.adapter(p6.storage.events.IStore)(
                p6.api.deinstify(self.__wrapStore))
            )

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
