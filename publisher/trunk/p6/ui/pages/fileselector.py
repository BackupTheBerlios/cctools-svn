"""Basic file selector page; published ItemSelected events."""

import wx
import wx.xrc
from wx.xrc import XRCCTRL

import zope.interface
import ccwx.xrcwiz

import p6
import p6.api

class FileDropTarget(wx.FileDropTarget):
    """ This object implements generic drop target functionality for Files """

    def OnDropFiles(self, x, y, filenames):
        """Bridge dropped files to P6 events."""

        # XXX we don't handle dropped directories here.
        
        for filename in filenames:
            zope.component.handle(
                p6.storage.events.ItemSelected(
                   p6.storage.items.FileItem(filename)
                   )
                )

class FileSelectorPage(ccwx.xrcwiz.XrcWizPage):
    """Page which displays a file selector and publishes events when
    items are selected or deselected.
    """
    zope.interface.implements(p6.ui.interfaces.IWizardPage)

    def __init__(self, parent, headline='Select Your Files'):
        """
        @param parent: Parent window
        @type parent: L{wx.Window}

        @param headline: Title to display above the wizard page
        @type headline: String
        """
        
        ccwx.xrcwiz.XrcWizPage.__init__(self, parent,
                                        self.PAGE_XRC, self.XRCID, headline)

        # connect event handlers for file browser, drag n drop, etc
        self.Bind(wx.EVT_BUTTON, self.onBrowse, XRCCTRL(self, "CMD_BROWSE"))
        
        # listen for item addition events
        zope.component.provideHandler(
            zope.component.adapter(p6.storage.events.IItemSelected)(
                p6.api.deinstify(self.selectItem))
            )

        # enable dropping files on the list box
        XRCCTRL(self, "LST_FILES").SetDropTarget(FileDropTarget())

    def selectItem(self, event):
        """Responds to ItemSelected events and updates the user interface."""
        XRCCTRL(self, "LST_FILES").\
                      InsertImageStringItem(0, event.item.getIdentifier(), 0)
    
    def onBrowse(self, event):
        """Event handler for file selection; publishes ItemSelected events
        when the user picks one or more files."""
        
        fileBrowser = wx.FileDialog(self.GetParent())

        if fileBrowser.ShowModal() == wx.ID_OK:

            for filename in fileBrowser.GetPaths():
                # generate an ItemSelected event for each file
                zope.component.handle(
                    p6.storage.events.ItemSelected(
                       p6.storage.items.FileItem(filename)
                       )
                    )

    def validate(self, event):
        return XRCCTRL(self, "LST_FILES").GetItemCount() > 0
    

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
