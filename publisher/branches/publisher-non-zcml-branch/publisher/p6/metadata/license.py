"""Interfaces for marking License Selector fields as special case.
See XXX for more information on custom field and group classes.
"""

import zope.interface

import interfaces
import base
import p6.metadata
import p6.storage

class ILicenseGroup(interfaces.IMetadataGroup):
    """Placeholder interface for differentiating between regular groups and
    license-selector metadata groups."""

class LicenseGroup(base.MetadataGroup):
    zope.interface.implements(ILicenseGroup, )
