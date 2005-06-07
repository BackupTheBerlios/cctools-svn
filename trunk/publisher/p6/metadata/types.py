"""Metadata field type declarations and associated adapters."""

import zope.interface
import zope.component

import p6.ui.interfaces
import interfaces

class ITextField(zope.interface.Interface):
    pass

class ISelectionField(zope.interface.Interface):
    pass

class IPasswordField(zope.interface.Interface):
    pass

class IBooleanField(zope.interface.Interface):
    pass

