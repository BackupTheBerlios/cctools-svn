import zope.interface

import interfaces
import base
import p6.metadata
import p6.storage

class ILicenseGroup(interfaces.IMetadataGroup):
    pass

class LicenseGroup(base.metadatagroup(p6.storage.interfaces.IWork)):
    zope.interface.implements(ILicenseGroup, )
