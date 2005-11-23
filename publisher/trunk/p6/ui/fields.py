"""
Adapters from MetadataField type interfaces to actual widgets.

Each adapter is expected to return a class object which can be called with
a single parameter -- the parent window -- to instantiate.  Additionally,
each class should have a getValue method which returns the current value.

XXX These classes should really adhere to a common interface.

See configure.zcml for registration details.
"""

import wx

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
    """Proxied combo box class with GetStringSelection mapped to getValue."""
    
    class ProxiedCombo(wx.ComboBox):
        def __init__(self, parent):
            wx.ComboBox.__init__(self, parent, choices=field.choices)

        def getValue(self):
            return self.GetStringSelection()

    return ProxiedCombo

def checkField(field):
    """Basic checkbox field."""
    
    return wx.CheckBox
