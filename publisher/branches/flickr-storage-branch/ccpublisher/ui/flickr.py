"""User interface connector for Flickr uploader"""

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
    
    def __init__(self, parent, storage):
        ccwx.xrcwiz.XrcWizPage.__init__(self, parent,
                                        os.path.join(p6.api.getResourceDir(),
                                                     "ccpublisher.xrc"),
                                        'FLICKR_WARNING', _('Authentication'))

        # connect the Authentication handler, finish page
        self.Bind(wx.EVT_BUTTON, self.onAuth, XRCCTRL(self, "CMD_AUTH_FLKR"))
        self.__storage = storage
        self.changed = False

    #on Authentication, make an Uploadr object and authenticate
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
                                        'FLICKR_COMPLETE', _('Uploading...'))


        self.__storage = storage
        
    def onChanged(self, event):
        # call the uploader and everything
        self.__storage.store()