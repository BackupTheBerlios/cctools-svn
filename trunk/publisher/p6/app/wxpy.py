import wx

import zope.interface

import p6
import interfaces

class WizApp(wx.App):
    zope.interface.implements(interfaces.IWizardApp)
    def __init__(self, appname=None, filename=None,
                 xrcfile=None, frameclass=p6.ui.wizard.WizFrame,
                 confFile='app.zcml'):

        # initialize the metadata group list
        self.groups = []
        self.items = []
        
        self.appname = appname
        self.errlog = filename
        self.xrcfile = xrcfile
        self.__frameclass = frameclass
        self.confFile = confFile

        wx.App.__init__(self, filename=self.errlog)

    def OnInit(self):
        # load your configuration
        self.context = zope.configuration.xmlconfig.file(self.confFile)
        
        self.SetAppName(self.appname)

        wx.InitAllImageHandlers()

        self.main = self.__frameclass(self)
        self.main.Show(True)

        self.SetTopWindow(self.main)

        return True
