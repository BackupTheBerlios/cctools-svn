import zope.interface

import interfaces
import base
import p6.metadata

class ILicenseGroup(interfaces.IMetadataGroup):
    pass

class LicenseGroup(base.MetadataGroup):
    zope.interface.implements(ILicenseGroup, )
