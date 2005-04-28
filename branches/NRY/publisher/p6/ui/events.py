import zope.interface

class IUpdateStatus(zope.interface.Interface):
    message = zope.interface.Attribute("")
    value = zope.interface.Attribute("")
    delta = zope.interface.Attribute("")

class UpdateStatusEvent:
    zope.interface.implements(IUpdateStatus)

    def __init__(self, message='', value=0, delta=0):
        self.message = message
        self.value = value
        self.delta = delta
