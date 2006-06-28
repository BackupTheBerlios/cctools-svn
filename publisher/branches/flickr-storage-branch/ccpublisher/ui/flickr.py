"""Self-Hosted Storage user interface components"""

import os
import sys
import webbrowser

import wx
import wx.html
import wx.lib.hyperlink
from wx.xrc import XRCCTRL

import ccwx
import p6.api
from p6.i18n import _

from ccpublisher.const import version
import ccpublisher.Uploadr as Uploadr

class WarningPage(ccwx.xrcwiz.XrcWizPage):
    """Final page for self-hosting storage provider"""

    def __init__(self, parent, storage):
        ccwx.xrcwiz.XrcWizPage.__init__(self, parent,
                                        os.path.join(p6.api.getResourceDir(),
                                                     "ccpublisher.xrc"),
                                        'FLICKR_WARNING', _('Complete'))

        # connect the Save button handler
        self.Bind(wx.EVT_BUTTON, self.onAuth, XRCCTRL(self, "CMD_AUTH_RDF"))
        self.__storage = storage
        self.changed = False

    def onAuth(self, event):
        """Allow the user to save the RDF block."""
        upT=Uploadr.Uploadr()
        upT.authenticate()

class FinalPage(ccwx.xrcwiz.XrcWizPage):
    """Final page for self-hosting storage provider"""

    def __init__(self, parent, storage):
        ccwx.xrcwiz.XrcWizPage.__init__(self, parent,
                                        os.path.join(p6.api.getResourceDir(),
                                                     "ccpublisher.xrc"),
                                        'FLICKR_COMPLETE', _('Upload Complete'))


        self.__storage = storage
        
    def onChanged(self, event):

        # generate the RDF
        self.__storage.store()
        
        # update the verification URL
        #XRCCTRL(self, "LBL_V_URL").SetLabel(self.__storage.verification_url)
        
        # update the RDF
        #XRCCTRL(self, "TXT_RDF").SetValue(self.__storage.rdf)
