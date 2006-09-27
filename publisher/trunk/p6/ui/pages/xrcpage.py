"""Generic page class for defining custom XRC-based pages."""

import wx
from wx.xrc import XRCCTRL

import zope.interface
import zope.component

import p6
import p6.metadata
import p6.ui.wizard

def xrcpage(title, xrcfile, xrcid):
    """Adapter which returns a callable which takes one parameter, the
    parent, and generates the L{XrcPage}.  This allows us to pass in the
    other parameters earlier, and delay actual construction until we
    have a parent created.
    """
    
    return lambda x: p6.ui.wizard.XRCWizardPage(x, title, xrcfile, xrcid)
