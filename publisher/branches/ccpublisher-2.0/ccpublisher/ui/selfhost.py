"""Self-Hosted Storage user interface components"""

import os
import webbrowser

import wx
import wx.html
import wx.lib.hyperlink
from wx.xrc import XRCCTRL

import ccwx
import p6.api

from ccpublisher.const import version

class FinalPage(ccwx.xrcwiz.XrcWizPage):
    """Final page for self-hosting storage provider"""

    def __init__(self, parent, storage):
        ccwx.xrcwiz.XrcWizPage.__init__(self, parent,
                                        self.PAGE_XRC,
                                        'SELFHOST_COMPLETE', 'Complete')

        # connect the Save button handler
        self.Bind(wx.EVT_BUTTON, self.onSave, XRCCTRL(self, "CMD_SAVE_RDF"))

        self.__storage = storage
        
    def onChanged(self, event):

        # generate the RDF
        self.__storage.store()
        
        # update the verification URL
        XRCCTRL(self, "LBL_V_URL").SetLabel(self.__storage.verification_url)
        
        # update the RDF
        XRCCTRL(self, "TXT_RDF").SetValue(self.__storage.rdf)

    def onSave(self, event):
        """Allow the user to save the RDF block."""

        saveDialog = wx.FileDialog(self, style=wx.SAVE|wx.OVERWRITE_PROMPT,
                                   wildcard="HTML (*.html)|*.html|"
                                            "Text files (*.txt)|*.txt")
        if (saveDialog.ShowModal() == wx.ID_OK):
            file(saveDialog.GetPath(), 'w').write(
                XRCCTRL(self, "TXT_RDF").GetValue())
            
            
    PAGE_XRC="""
<resource>
  <object class="wxPanel" name="SELFHOST_COMPLETE">
    <object class="wxFlexGridSizer">
      <cols>1</cols>
      <object class="sizeritem">
        <object class="wxStaticText">
          <label>This is your verification RDF.</label>
        </object>
      </object>
      <object class="sizeritem">
        <object class="wxStaticText" name="LBL_VRDF_DEST">
          <label>Copy and paste the text below into the document at </label>
        </object>
        <flag>wxEXPAND|wxALL</flag>
      </object>
      <object class="sizeritem">
        <object class="wxStaticText" name="LBL_V_URL">
          <label>Blarf</label>
        </object>
        <flag>wxEXPAND|wxALL</flag>
      </object>
      <object class="sizeritem">
        <object class="wxStaticText">
          <label>After you paste the verification text into your web page, your file is ready\nto file share; just drop it in your shared folder.</label>
        </object>
      </object>
      <object class="sizeritem">
        <object class="wxButton" name="CMD_SAVE_RDF">
          <label>Save</label>
        </object>
        <flag>wxALIGN_RIGHT</flag>
      </object>
      <object class="sizeritem">
        <object class="wxTextCtrl" name="TXT_RDF">
          <style>wxTE_MULTILINE|wxTE_READONLY</style>
        </object>
        <flag>wxALL|wxGROW</flag>
      </object>
      <vgap>5</vgap>
      <growablecols>0</growablecols>
      <growablerows>5</growablerows>
    </object>
  </object>
</resource>
"""
