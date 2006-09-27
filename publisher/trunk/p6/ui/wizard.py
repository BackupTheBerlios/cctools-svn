"""
Customized wizard framework -- top level window classes.
"""

import sys

import wx
import wx.wizard
import wx.xrc

import zope.interface
import zope.configuration.xmlconfig

import p6
import p6.api
import p6.ui.xrc
import interfaces
import pagecollection

def call_sink(*args, **kwargs):
    pass

def makeHeader(wizPg, title):
    sizer = wx.BoxSizer(wx.VERTICAL)
    wizPg.SetSizer(sizer)
    title = wx.StaticText(wizPg, -1, title)
    title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
    sizer.Add(title, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    sizer.Add(wx.StaticLine(wizPg, -1), 0, wx.EXPAND|wx.ALL, 5)
    return sizer

class P6WizardPage(wx.wizard.PyWizardPage):
    def __init__(self, parent, title):
        wx.wizard.PyWizardPage.__init__(self, parent)
        self.sizer = makeHeader(self, title)

    @property
    def __list(self):
        # XXX lookup utility?
        return p6.api.getApp().pages

    pagelist = __list
    
    def GetNext(self):

        print "in GetNext "

        if self.__list.is_last():
            return None
        else:
            return self.__list.next()(self.GetParent())
    
    def GetPrev(self):

        print "in getprev"
        
        if self.__list.is_first():
            return None
        else:
            return self.__list.previous()(self.GetParent())
      
    def validate(self, event):
        
        return True

    def onChanging(self, event):
        pass

    def onChanged(self, event):
        pass

class XRCWizardPage(P6WizardPage):
    def __init__(self, parent, title, xrcfile, xrcid ):
        P6WizardPage.__init__(self, parent, title)

        # load the user interface
        self.__loadXrcUi(xrcfile, xrcid)

    def __loadXrcUi(self, xrcfile, xrcid):

        self.sizer.Add(p6.ui.xrc.load(xrcfile).LoadPanel(self, xrcid),
                       flag = wx.EXPAND)

class P6Wizard(wx.wizard.Wizard):
    def __init__(self, parent, id, title, pagelist=None):
        wx.wizard.Wizard.__init__(self, parent, id, title)

        # store a reference to the page collection
        self.setModel(pagelist)
        print len(self.getModel())
        
        # attach event handlers
        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, self.OnWizardPageChanged)
        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGING, self.OnWizardPageChanging)
        self.Bind(wx.wizard.EVT_WIZARD_CANCEL, self.OnWizardCancel)

    def start(self):
        print self.__pages.current()(self)
        self.RunWizard(self.__pages[0](self))
        
    def setModel(self, pagelist):

        if pagelist is None:
            pagelist = p6.api.getApp().pages
            
        if isinstance(pagelist, list):
            self.__pages = pagecollection.PageCollection(pagelist)
        else:
            self.__pages = pagelist

    def getModel(self):
        """Return the PageCollection model used for this wizard."""
        return self.__pages

    def OnWizardPageChanged(self, event):
        
        getattr(event.GetPage(), 'onChanged', call_sink)(event)

    def OnWizardPageChanging(self, event):
        getattr(event.GetPage(), 'validate', call_sink)(event)

        if event.IsAllowed():
            getattr(event.GetPage(), 'onChanging', call_sink)(event)

    def OnWizardCancel(self, event):
        sys.exit()
