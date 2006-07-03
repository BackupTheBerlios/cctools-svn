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
        storage_registry = zope.component.getUtility(
            p6.storage.registry.IStorageRegistry)

        # iterate through list and add each to the UI
        for p_id in storage_registry.identifiers():

            # get a handle to the storage provider
            provider = storage_registry[p_id]
            
            # set the first item to wx.RB_GROUP to make them mutually exclusive
            if p_id == storage_registry.identifiers()[0]:
                style = wx.RB_GROUP
            else:
                style = 0

            # create the new radio button
            rdbItem = wx.RadioButton(self, label=_(provider.name), style=style)
            rdbItem.id = provider.id

            self.__options.append(rdbItem)
            self.GetSizer().Add(rdbItem)

            # create the description text
            desc_sizer = wx.FlexGridSizer(1, 2)
            desc_sizer.AddGrowableCol(1)
            desc_sizer.AddGrowableRow(0)
            desc_sizer.AddSpacer((20, 5))
            desc_sizer.Add(wx.StaticText(self, -1,
                                      _(provider.description),
                                      style=wx.EXPAND))
            self.GetSizer().Add(desc_sizer)
    
    def onChanged(self, event):
        if event.direction:
            self.init()

    def onChanging(self, event):
        # activate the selected provider and declare the others deactivated

        storage_registry = zope.component.getUtility(
            p6.storage.registry.IStorageRegistry)

        for rdbOption in self.__options:

            if rdbOption.GetValue():
                storage_registry[rdbOption.id].activate()
            else:
                storage_registry[rdbOption.id].deactivate()

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


