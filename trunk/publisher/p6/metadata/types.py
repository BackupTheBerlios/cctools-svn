"""Metadata field type declarations and associated adapters."""

import wx

import zope.interface
import zope.component

import p6.ui.interfaces
import interfaces

class ITextField(zope.interface.Interface):
    pass

class ISelectionField(zope.interface.Interface):
    pass

# Field type to Entry Widget Adapters
def textField(field):
    return wx.TextCtrl

def comboField(field):
    class ProxiedCombo(wx.ComboBox):
        def __init__(self, parent):
            wx.ComboBox.__init__(self, parent, choices=field.choices)

        def getValue(self):
            return self.GetStringSelection()

    return ProxiedCombo


