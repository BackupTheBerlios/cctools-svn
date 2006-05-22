import zope.component
import zope.interface

import p6

class CommonStorageMixin(object):
    def registerEvents(self):
        
        zope.component.provideHandler(
            zope.component.adapter(p6.storage.events.IValidate)(
                p6.api.deinstify(self.validate))
            )

        zope.component.provideHandler(
            zope.component.adapter(p6.storage.events.IStore)(
                p6.api.deinstify(self.__wrapStore))
            )

    def activated(self):
        """Return True if self has been decorated with the IActivated
        interface."""

        return (p6.extension.interfaces.IActivated in
                zope.interface.directlyProvidedBy(self))

    def validate(self, event=None):
        """Handle L{p6.storage.events.IValidate} events by simply
        updating the progress bar."""

    def __wrapStore(self, event=None):
        """Wraps dispatch of L{p6.storage.events.IStore} events by calling
        self.store(self, event).  Publishes a L{p6.storage.events.WorkStored}
        event after .store completes.
        """

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

        return {}
