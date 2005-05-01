import wx

import zope.interface
import zope.component

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

        self.connectEvents()
        
        return True

    def connectEvents(self):

        # listen for item addition events
        zope.component.provideHandler(
            zope.component.adapter(p6.storage.events.IItemSelected)(
                p6.api.deinstify(self.selectItem))
            )

        # create the root item
        self.items.append(p6.storage.items.RootItem())
        
    def selectItem(self, event):
        self.items.append(event.item)

