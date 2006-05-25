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
                                        os.path.join(p6.api.getResourceDir(),
                                                     "ccpublisher.xrc"),
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
            
            
