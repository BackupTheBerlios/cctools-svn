import wx
from wx.xrc import XRCCTRL

import ccwx.xrcwiz

import zope.component

import p6
import p6.api

class StorePage(ccwx.xrcwiz.XrcWizPage):
    """Displays a page which validates and stores the item."""
    
    XRCID = "STORE_PROGRESS"

    def __init__(self, parent, headline='Uploading'):
        ccwx.xrcwiz.XrcWizPage.__init__(self, parent,
                                        self.PAGE_XRC, self.XRCID, headline)

        # register event handlers
        zope.component.provideHandler(
            zope.component.adapter(p6.storage.events.IStored)(
                p6.api.deinstify(self.postStore))
            )

        zope.component.provideHandler(
            zope.component.adapter(p6.ui.events.IUpdateStatus)(
                p6.api.deinstify(self.updateStatus))
            )

        zope.component.provideHandler(
            zope.component.adapter(p6.ui.events.IResetStatus)(
                p6.api.deinstify(self.resetStatus))
            )

    def onChanged(self, event):
        # disable the next button during the storage process
        # and use busy cursor
        XRCCTRL(wx.GetApp().GetTopWindow(), "CMD_NEXT").Disable()
        wx.BeginBusyCursor()

        wx.YieldIfNeeded()
        self.validateItem()

        wx.YieldIfNeeded()
        self.store()

    def validateItem(self):
        v_event = p6.storage.events.ValidateWork()
        
        zope.component.handle(v_event)

        if len(v_event.errors) > 0:
            print 'Aieeee!'

    def store(self):
        event = p6.storage.events.StoreWork()
        zope.component.handle(event)

    def postStore(self, event):
        # re-enable the next button
        event = p6.ui.events.UpdateStatusEvent(value=0, message='Complete.')
        zope.component.handle(event)
        
        XRCCTRL(wx.GetApp().GetTopWindow(), "CMD_NEXT").Enable()
        wx.EndBusyCursor()

        self.Refresh()

    def updateStatus(self, event):
        new_value = 0
        
        if event.value != 0:
            new_value = event.value

        if event.delta != 0:
            new_value = XRCCTRL(self, "WXG_PROGRESS").GetValue() + event.delta

        XRCCTRL(self, "WXG_PROGRESS").SetValue(new_value)
        XRCCTRL(self, "LBL_CURRENTLY").SetLabel(event.message)

    def resetStatus(self, event):
        XRCCTRL(self, "WXG_PROGRESS").SetValue(0)
        XRCCTRL(self, "WXG_PROGRESS").SetRange(event.steps)

        XRCCTRL(self, "LBL_CURRENTLY").SetLabel(event.message)
        

    PAGE_XRC = """
<resource>
  <object class="wxPanel" name="STORE_PROGRESS">
    <object class="wxFlexGridSizer">
      <cols>1</cols>
      <growablecols>0</growablecols>
      <growablerows>4</growablerows>
      <vgap>10</vgap>
      
      <object class="sizeritem">
        <object name="LBL_MACRO_TASK" class="wxStaticText">
          <label>Validating input...</label>
        </object>
        <flag>wxEXPAND</flag>
      </object>
      
      <object class="sizeritem">
        <object class="wxStaticText" name="LBL_CURRENTLY">
          <label/>
        </object>
        <flag>wxEXPAND</flag>
      </object>

      <object class="sizeritem">
        <object class="wxGauge" name="WXG_PROGRESS">
          <range>100</range>
          <style>wxGA_PROGRESSBAR</style>
        </object>
        <flag>wxEXPAND</flag>
      </object>
      
    </object>
  </object>

</resource>
    """
    
