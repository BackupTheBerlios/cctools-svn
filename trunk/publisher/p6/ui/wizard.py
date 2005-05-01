import wx
import wx.xrc

import zope.interface
import zope.configuration.xmlconfig
import ccwx.xrcwiz

import p6
import p6.api
import interfaces

class WizFrame(ccwx.xrcwiz.XrcWiz):
    def __init__(self, xrcid, app):
        ccwx.xrcwiz.XrcWiz.__init__(self, app, app.xrcfile, xrcid)

        self.app = app
        self.setPages([n(self) for n in p6.api.getApp().pages])

    def setPages(self, pages):
        self.pages = pages

        self.cur_page = 0
        self.addCurrent(None)

        self.pages[self.cur_page].Show()

        self.SetAutoLayout(True)
        self.Show()
        self.Layout()
                
    def getPageParent(self):
        """Return the object which should serve as parent for page objects."""
        return wx.xrc.XRCCTRL(self, "PNL_BODY")
    
