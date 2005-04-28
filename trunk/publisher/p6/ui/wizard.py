import wx
import wx.xrc

import zope.interface
import zope.configuration.xmlconfig
import ccwx.xrcwiz

import interfaces

class WizFrame(ccwx.xrcwiz.XrcWiz):
    def __init__(self, xrcid, app):
        ccwx.xrcwiz.XrcWiz.__init__(self, app, app.xrcfile, xrcid)

        self.app = app

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
    
class WizApp(wx.App):
    zope.interface.implements(interfaces.IWizardApp)
    def __init__(self, appname=None, filename=None,
                 xrcfile=None, frameclass=WizFrame,
                 confFile='app.zcml'):

        # initialize the metadata group list
        self.groups = []

        # load your configuration
        self.context = zope.configuration.xmlconfig.file(confFile)
        
        self.appname = appname
        self.errlog = filename
        self.xrcfile = xrcfile
        self.__frameclass = frameclass

        wx.App.__init__(self, filename=self.errlog)

    def OnInit(self):
        self.SetAppName(self.appname)

        wx.InitAllImageHandlers()

        self.main = self.__frameclass(self)
        self.main.Show(True)

        self.SetTopWindow(self.main)

        return True