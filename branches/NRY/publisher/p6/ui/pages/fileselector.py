
import wx
import wx.xrc
from wx.xrc import XRCCTRL

import p6
import p6.storage
import zope.interface
import p6.ui.wizard
import ccwx.xrcwiz
import p6.ui.interfaces

class FileSelectorPage(ccwx.xrcwiz.XrcWizPage):
    zope.interface.implements(p6.ui.interfaces.IWizardPage)

    def __init__(self, parent, headline='Select Your Files'):
        ccwx.xrcwiz.XrcWizPage.__init__(self, parent,
                                        self.PAGE_XRC, self.XRCID, headline)

        # connect event handlers for file browser, drag n drop, etc
        self.Bind(wx.EVT_BUTTON, self.onBrowse, XRCCTRL(self, "CMD_BROWSE"))
        
        # listen for item addition events
        zope.component.provideHandler(
            zope.component.adapter(p6.storage.events.IItemSelected)(
                p6.deinstify(self.selectItem))
            )

    @zope.component.adapter(p6.storage.events.IItemSelected)
    @p6.deinstify
    def selectItem(self, event):
        XRCCTRL(self, "LST_FILES").\
                      InsertImageStringItem(0, event.item.getIdentifier(), 0)
    
    def onBrowse(self, event):
        fileBrowser = wx.FileDialog(self.GetParent())

        if fileBrowser.ShowModal() == wx.ID_OK:

            for filename in fileBrowser.GetPaths():
                # generate an ItemSelected event for each file
                zope.component.handle(
                    p6.storage.events.ItemSelected(
                       p6.storage.items.FileItem(filename)
                       )
                    )

    XRCID = "FILE_SELECTOR"
    PAGE_XRC = """
<resource>
  <object class="wxPanel" name="FILE_SELECTOR">
    <object class="wxFlexGridSizer">
      <cols>1</cols>
      <object class="sizeritem">
        <object class="wxStaticText" name="LBL_DROPFILES">
          <label>Drag n' drop the audio or video files you want to publish to the 
Web with a Creative Commons license, or click the Browse button 
to manually select your files.</label>
        </object>
        <cellpos>0,0</cellpos>
        <cellspan>1,1</cellspan>
        <flag>wxEXPAND</flag>
      </object>
      <object class="sizeritem">
        <object class="wxFlexGridSizer">
          <cols>3</cols>
          <hgap>5</hgap>
          <object class="sizeritem">
            <object class="wxButton" name="CMD_BROWSE">
              <label>Browse</label>
            </object>
            <flag>wxALIGN_BOTTOM</flag>
            <cellpos>2,0</cellpos>
            <cellspan>1,1</cellspan>
          </object>
          <object class="sizeritem">
            <object class="wxButton" name="CMD_DELETE">
              <label>Delete</label>
            </object>
            <flag>wxALIGN_BOTTOM</flag>
          </object>
          <object class="spacer">
            <size>1,1</size>
          </object>
          <growablecols>1</growablecols>
          <growablecols>2</growablecols>
        </object>
        <flag>wxALIGN_RIGHT</flag>
        <border>05</border>
        <cellpos>2,0</cellpos>
        <cellspan>1,1</cellspan>
      </object>
      <object class="sizeritem">
        <object class="wxListCtrl" name="LST_FILES">
          <size>450,175</size>
          <style>wxLC_ICON|wxSIMPLE_BORDER</style>
        </object>
        <cellpos>1,0</cellpos>
        <cellspan>1,1</cellspan>
      </object>
      <growablerows>2</growablerows>
      <vgap>5</vgap>
      <growablecols>0</growablecols>
    </object>
  </object>
</resource>
    """