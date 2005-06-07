import wx

# Field type to Entry Widget Adapters
def textField(field):
    return wx.TextCtrl

def passwordField(field):
    class ProxiedPasswordField(wx.TextCtrl):
        def __init__(self, parent):
            wx.TextCtrl.__init__(self, parent, style=wx.TE_PASSWORD)

    return ProxiedPasswordField

def comboField(field):
    class ProxiedCombo(wx.ComboBox):
        def __init__(self, parent):
            wx.ComboBox.__init__(self, parent, choices=field.choices)

        def getValue(self):
            return self.GetStringSelection()

    return ProxiedCombo

def checkField(field):
    return wx.CheckBox
