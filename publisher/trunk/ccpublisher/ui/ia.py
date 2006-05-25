"""ccPublisher-specific user interface components."""

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
    """Welcome page class."""

    HTTP_LINK_VALUE = None
    
    def __init__(self, parent, storage):
        ccwx.xrcwiz.XrcWizPage.__init__(self, parent,
                                        os.path.join(p6.api.getResourceDir(),
                                                     "ccpublisher.xrc"),
                                        'IA_COMPLETE', 'Upload Complete')

        self.storage = storage
        
        # When we change the place holder label to a link label,
        # we store a reference here for handling future updates
        self.__http_link = None

        # Check if we have a link to use
        if self.HTTP_LINK_VALUE is not None:
            self.setItemUrl(self.HTTP_LINK_VALUE)

    def onChanged(self, event):
        """Update the display with the link to the item online."""

        self.setItemUrl(self.storage.uri)

        
    def setItemUrl(self, url):
        """Update the display with a link to the item online."""

        if self.__http_link is None:
            # substitute the link label for the place holder

            # create the new link
            self.__http_link = wx.lib.hyperlink.HyperLinkCtrl(self, -1, url)
            
            # insert it into the sizer
            self.GetSizer().Add(self.__http_link)
            
        else:
            self.__http_link.SetLabel(url)
            self.__http_link.SetURL(url)

        # force the window to redraw
        self.Fit()
