"""
Adapters from MetadataField type interfaces to actual widgets.

Each adapter is expected to return a class object which can be called with
a single parameter -- the parent window -- to instantiate.  Additionally,
each class should have a getValue method which returns the current value.

XXX These classes should really adhere to a common interface.

See configure.zcml for registration details.
"""

import wx

from p6.i18n import _

def textField(field):
    """Basic text input widget."""
    
    return wx.TextCtrl

def passwordField(field):
    """Proxied text input widget with password style set."""
    
    class ProxiedPasswordField(wx.TextCtrl):
        def __init__(self, parent):
            wx.TextCtrl.__init__(self, parent, style=wx.TE_PASSWORD)

    return ProxiedPasswordField

def comboField(field):
    """Proxied combo box class with additional error handling in GetValue
    to catch errors on OS X.  Proxied class also provides i18n support."""

    class ProxiedCombo(wx.ComboBox):
        def __init__(self, parent):
            wx.ComboBox.__init__(self, parent,
                                 style=wx.CB_READONLY)
            # XXX we should support type-ahead find here

            # append each item to the list, associating each translated
            # item with it's message id
            for choice in field.choices:
                self.Append(_(choice), choice)

        def GetValue(self):
            """Return the message id of the selected item, or an empty
            string if no item is selected."""
            
            if self.GetSelection() == wx.NOT_FOUND:
                return ""
            else:
                return self.GetClientData(self.GetSelection())

        def SetValue(self, new_value):
            """Set the string selection to the translated value."""

            self.SetStringSelection(_(new_value))
            
    return ProxiedCombo

def checkField(field):
    """Basic checkbox field."""
    
    return wx.CheckBox
