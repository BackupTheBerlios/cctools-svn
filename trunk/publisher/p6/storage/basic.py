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
                p6.api.deinstify(self.store))
            )

    def validate(self, event=None):
        """Handle L{p6.storage.events.IValidate} events by simply
        updating the progress bar."""
        
        update = p6.ui.events.UpdateStatusEvent(delta=20,
                                                message='in Validate...')

        zope.component.handle(update)

    def store(self, event=None):
        """Handle L{p6.storage.events.IStore} events by simply
        updating the progress bar; fire a L{p6.storage.events.WorkStored}
        event after the "storage" process is complete.
        """
        
        update = p6.ui.events.UpdateStatusEvent(delta=20,
                                                message='in Store...')

        zope.component.handle(update)


        # after the storage process, publish a post-store event
        event = p6.storage.events.WorkStored()
        zope.component.handle(event)
