import wx
import wx.xrc

import p6

class P6PrefsPanel(wx.Panel):
    def __init__(self, parent, id, prefs):
        self.id = id
        
        res = wx.xrc.EmptyXmlResource()
        res.LoadFromString(self.XRC)

        # create the frame's skeleton
        pre = wx.PrePanel()

        # load the actual definition from the XRC
        res.LoadOnPanel(pre, parent, 'PREFPANEL')

        # finish creation
        self.PostCreate(pre)
        self.SetAutoLayout(True)

        # layout UI elements
        self.fields = {}
        for fieldid in prefs:
            # create the label
            self.GetSizer().Add(wx.StaticText(self,
                                              label=prefs[fieldid].label))

            # create the widget
            if prefs[fieldid].type == str:
                # string preference
                widget = wx.TextCtrl(self)

                if prefs[fieldid].value is not None:
                    widget.SetValue(prefs[fieldid].value)
                    
                self.fields[fieldid] = widget

                self.GetSizer().Add(widget, flag=wx.EXPAND)

    def _saveToApp(self):
        """Persist values back to the application object."""
        for field in self.fields:
            p6.api.updatePref(self.id, field, self.fields[field].GetValue())
        

    XRC = """
<resource>
  <object class="wxPanel" name="PREFPANEL">
    <object class="wxFlexGridSizer">
      <cols>2</cols>
      <growablecols>1</growablecols>
    </object>
  </object>
</resource>
"""

class P6PrefsWindow(wx.Frame):
    def __init__(self, parent):
        res = wx.xrc.XmlResource(
            os.path.join(p6.api.getResourceDir(), 'p6.xrc'))

        # create the frame's skeleton
        pre = wx.PreFrame()

        # load the actual definition from the XRC
        res.LoadOnFrame(pre, parent, 'FRM_PREFS')

        # finish creation
        self.PostCreate(pre)
        self.SetAutoLayout(True)

        # load the preference pages
        self.pages = []
        notebook = wx.xrc.XRCCTRL(self, 'NTB_PREFS')

        prefdict = p6.api.getApp().prefs
        for id in prefdict:
            self.pages.append(P6PrefsPanel(notebook, id, prefdict[id].fields))
            notebook.AddPage(self.pages[-1], prefdict[id].label)

        # connect events
        self.Bind(wx.EVT_BUTTON, self.onOK, wx.xrc.XRCCTRL(self,'CMD_OK'))
        self.Bind(wx.EVT_BUTTON, self.onCancel, wx.xrc.XRCCTRL(self,'CMD_CANCEL'))
        
        self.Fit()

    def onOK(self, event):
        # store the preference settings back to the application
        for page in self.pages:
            page._saveToApp()

        self.Close()

    def onCancel(self, event):
        self.Close()

