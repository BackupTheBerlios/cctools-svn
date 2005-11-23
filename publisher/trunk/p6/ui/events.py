"""
User interface events and associated interfaces published to notify
other portions of the P6 framework of user interaction.
"""

import zope.interface

class IUpdateStatus(zope.interface.Interface):
    """IUpdateStatus events are published to let the interface
    know when to increment the progress bar.
    """
    
    message = zope.interface.Attribute("")
    value = zope.interface.Attribute("")
    delta = zope.interface.Attribute("")

class IResetStatus(zope.interface.Interface):
    """IResetStatus events are published to instruct the user interface
    to reset progress bars."""
    
    message = zope.interface.Attribute("")
    steps = zope.interface.Attribute("")
    
class UpdateStatusEvent:
    """Basic implementation of an L{IUpdateStatusEvent}."""
    zope.interface.implements(IUpdateStatus)

    def __init__(self, message='', **kwargs):
        """
        @param message: The message to update the progress bar with.
        @keyword value: (optional) The absolute value to set the progress
           bar to.
        @keyword delta: (optional) The amount to increment the progress bar.
        """

        # XXX We should probably use None or something here to indicate the values weren't specified to allow for message changes w/o incrementing the bar
        self.message = message
        self.value = kwargs.get('value', 0)
        self.delta = kwargs.get('delta', 0)

class ResetStatusEvent:
    """Basic implementation of an L{IResetStatusEvent}."""
    zope.interface.implements(IResetStatus)

    def __init__(self, message='', steps=0):
        """
        @param message: The message to set the progress bar's status to.
        @param steps: The number of steps the progress bar will have;
           the bar is incremented by a "step" if it receives an
           L{UpdateStatusEvent} with no value or delta specified.
        """
        
        self.message = message
        self.steps = steps
        
