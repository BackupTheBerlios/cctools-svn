"""Generic page class for defining custom XRC-based pages."""

import wx
from wx.xrc import XRCCTRL
import ccwx

import zope.interface
import zope.component

import p6
import p6.metadata

class XrcPage(ccwx.xrcwiz.XrcWizPage):
    """Generic page class."""
    
    def __init__(self, parent, headline, xrcfile, xrcid):
        """
        @param parent: Parent window object
        @type  parent: L{wx.Window}

        @param headline: Text to display above this page
        @type  headline: String

        @param xrcfile: the source of the page's XRC; may be one of the
          following:
            - handle to a file-like object
            - String containing the XRC filename
            - String containing the XRC chunk

        @param xrcid: The ID of the object in the xrcfile to load as the page.
        @type  xrcid: String
        """
        
        ccwx.xrcwiz.XrcWizPage.__init__(self, parent,
                                        xrcfile, xrcid, headline)


def xrcpage(title, xrcfile, xrcid):
    """Adapter which returns a callable which takes one parameter, the
    parent, and generates the L{XrcPage}.  This allows us to pass in the
    other parameters earlier, and delay actual construction until we
    have a parent created.
    """
    
    return lambda x: XrcPage(x, title, xrcfile, xrcid)
