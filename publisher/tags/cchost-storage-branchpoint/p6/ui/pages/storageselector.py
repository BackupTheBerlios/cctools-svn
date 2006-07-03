"""Basic file selector page; published ItemSelected events."""

import wx
import wx.xrc
from wx.xrc import XRCCTRL

import zope.interface
import ccwx.xrcwiz

import p6
import p6.api
import p6.storage.interfaces
import p6.extension.interfaces

from p6.i18n import _

class StorageSelectorPage(ccwx.xrcwiz.XrcWizPage):
    """User interface page which displays a list of available
    storage providers and allows the user to select one or more.
    """
    zope.interface.implements(p6.ui.interfaces.IWizardPage)

    def __init__(self, parent, headline=_('Select Upload Destination'),
                 multi=True):
        """
        @param parent: Parent window
        @type parent: L{wx.Window}

        @param headline: Title to display above the wizard page
        @type headline: String
        """
        
        ccwx.xrcwiz.XrcWizPage.__init__(self, parent,
                                        self.PAGE_XRC, self.XRCID, headline)

        self._multi = multi
        
    def init(self):

        self.__options = []
        self.GetSizer().Clear()
        
        # get a list of storage providers
        providers = p6.api.getApp().storage
        provider_info = []

        # get the information for all providers
        for p in providers:
            provider_info.append( (p.id, p.name, p.description) )

        for p in provider_info:
            # XXX need to handle self._multi here
            
            # set the first item to wx.RB_GROUP to make them mutually exclusive
            if p == provider_info[0]:
                style = wx.RB_GROUP
            else:
                style = 0

            # create the new radio button
            rdbItem = wx.RadioButton(self, label=p[1], style=style)
            rdbItem.id = p[0]

            self.__options.append(rdbItem)
            self.GetSizer().Add(rdbItem)

            # create the description text
            desc_sizer = wx.FlexGridSizer(1, 2)
            desc_sizer.AddGrowableCol(1)
            desc_sizer.AddGrowableRow(0)
            desc_sizer.AddSpacer((20, 5))
            desc_sizer.Add(wx.StaticText(self, -1, p[2], style=wx.EXPAND))
            self.GetSizer().Add(desc_sizer)
    
    def onChanged(self, event):
        if event.direction:
            self.init()

    def onChanging(self, event):
        # store the provider selection by decorating classes with
        # IActivated or IDeactivated... XXX: we also need a way
        # to "undecorate" classes.

        for rdbOption in self.__options:
            provider = [n for n in p6.api.getApp().storage
                        if n.id == rdbOption.id][0]

            if rdbOption.GetValue():
                # this option is selected
                zope.interface.directlyProvides(provider,
                    p6.extension.interfaces.IActivated)
            else:
                # remove the IActivated interface if necessary
                zope.interface.directlyProvides(provider, 
                    p6.extension.interfaces.IDeactivated)

    def validate(self, event):
        return True
    

    XRCID = "STORAGE_SELECTOR"
    PAGE_XRC = """
<resource>
  <object class="wxPanel" name="%s">
    <object class="wxFlexGridSizer">
      <cols>1</cols>
      <vgap>5</vgap>
      <hgap>5</hgap>
      <growablecols>0</growablecols>
    </object>
  </object>
</resource>
    """ % XRCID


