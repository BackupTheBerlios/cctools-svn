import zope.interface

import interfaces
import base
import p6.metadata
import p6.storage

class ILicenseGroup(interfaces.IMetadataGroup):
    pass

def licensemetadatagroup(appliesTo=p6.storage.interfaces.IWork):
    class LicenseGroup(base.metadatagroup(appliesTo)):
        zope.interface.implements(ILicenseGroup, )

    return LicenseGroup
