"""Storage page for controlling upload process and displaying feedback."""

import os

import wx
from wx.xrc import XRCCTRL

import ccwx.xrcwiz

import zope.component

import p6
import p6.api

class FinalUrlPage(ccwx.xrcwiz.XrcWizPage):
    """Displays a page which validates and stores the item."""
    
    def __init__(self, parent, headline='Uploading'):
        """
        @param parent: Parent window
        @type parent: L{wx.Window}

        @param headline: Title to display above the wizard page
        @type headline: String
        """
        
        ccwx.xrcwiz.XrcWizPage.__init__(self, parent,
                                        os.path.join(p6.api.getResourceDir(),
                                                     "p6.xrc"),
                                        "FINAL_URL",
                                        headline)

