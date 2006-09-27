"""Storage page for controlling upload process and displaying feedback."""

import os

import wx
from wx.xrc import XRCCTRL

import zope.component

import p6
import p6.api
import p6.ui.wizard

from p6.i18n import _

class FinalUrlPage(p6.ui.wizard.XRCWizardPage):
    """Displays a page which validates and stores the item."""
    
    def __init__(self, parent, headline=_('Uploading')):
        """
        @param parent: Parent window
        @type parent: L{wx.Window}

        @param headline: Title to display above the wizard page
        @type headline: String
        """
        
        ccwx.xrcwiz.XRCWizardPage.__init__(self, parent, headline,
                                        os.path.join(p6.api.getResourceDir(),
                                                     "p6.xrc"),
                                        "FINAL_URL")

