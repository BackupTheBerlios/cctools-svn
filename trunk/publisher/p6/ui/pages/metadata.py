import weakref

import wx
import ccwx

import zope.component
import zope.interface

import p6.storage
import p6.metadata.events
import p6.metadata.interfaces

import license

class MetadataPage(ccwx.xrcwiz.XrcWizPage):
    zope.interface.implements(p6.ui.interfaces.IWizardPage)

    def __init__(self, parent, metaGroup):
        ccwx.xrcwiz.XrcWizPage.__init__(self, parent,
                                        self.PAGE_XRC % metaGroup.id,
                                        metaGroup.id,
                                        metaGroup.title)

        self.metagroup = metaGroup
        self.initFields(metaGroup)

    def initFields(self, metaGroup):
        """Create the user input widgets for this group."""

        for field in metaGroup.getFields():

            label = wx.StaticText(self, label=field.label)
            self.GetSizer().Add(label)

            widget = p6.ui.interfaces.IEntryWidget(field)(self)
            field._widget = weakref.ref(widget)
            
            self.GetSizer().Add(widget, flag=wx.EXPAND)

    def onChanging(self, event):
        """Perform storage of field values back to metadata framework."""
        
        for field in self.metagroup.getFields():
            widget = field._widget()

            if widget is not None:
                field.setValue(widget.GetValue())
                print field()
                
        
    PAGE_XRC = """
<resource>
  <object class="wxPanel" name="%s">
    <object class="wxFlexGridSizer">
      <cols>2</cols>
      <vgap>5</vgap>
      <hgap>5</hgap>
      <growablecols>1</growablecols>
    </object>
  </object>
</resource>
    """

class ItemMetadataPage(ccwx.xrcwiz.XrcWizPage):
    zope.interface.implements(p6.ui.interfaces.IWizardPage)

    def __init__(self, parent, metaGroup):
        ccwx.xrcwiz.XrcWizPage.__init__(self, parent,
                                        self.PAGE_XRC % metaGroup.id,
                                        metaGroup.id,
                                        metaGroup.title)

        self.metagroup = metaGroup
        self.__items = []
        self.initFields(self.metagroup)

        # bind P6 events
        zope.component.provideHandler(
            zope.component.adapter(p6.storage.events.IItemSelected)(
                p6.deinstify(self.onItemSelected))
            )
        
        # bind wx events
        self.Bind(ccwx.xrcwiz.EVT_XRCWIZ_PAGE_CHANGED, self.onChanged)

    def onItemSelected(self, event):
        self.__items.append(event.item)

    def onItemDeselected(self, event):
        del self.__items[self.__items.index(event.item)]

    def initFields(self, metaGroup):
        """Create the user input widgets for this group."""

        for field in metaGroup.getFields():
            field._widget = {}
            
        for item in self.__items:

            # create the item label
            item_label = wx.StaticText(self, label=item.getIdentifier())
            self.GetSizer().Add(item_label, flag=wx.EXPAND)

            # create the item sizer
            item_sizer = wx.FlexGridSizer(cols=2)
            item_sizer.AddGrowableCol(1)
            self.GetSizer().Add(item_sizer, flag=wx.EXPAND)
            
            for field in metaGroup.getFields():

                label = wx.StaticText(self, label=field.label)
                item_sizer.Add(label)

                widget = p6.ui.interfaces.IEntryWidget(field)(self)
                field._widget[item] = weakref.ref(widget)
                item_sizer.Add(widget, flag=wx.EXPAND)

    def onChanging(self, event):
        """Perform storage of field values back to metadata framework."""

        for item in self.__items:
            for field in self.metagroup.getFields():
                field_widget = field._widget[item]()

                if field_widget is not None:
                    field.setValue(field_widget.GetValue(), item=item)

    def onChanged(self, event):
        self.initFields(self.metagroup)
        
    PAGE_XRC = """
<resource>
  <object class="wxPanel" name="%s">
    <object class="wxFlexGridSizer">
      <cols>1</cols>
      <vgap>5</vgap>
      <hgap>5</hgap>
      <growablecols>1</growablecols>
    </object>
  </object>
</resource>
    """

def page_IWork(metaGroup, appliesTo):
    """Subscription adapter to adapt a metadata group to a wizard page."""
    if metaGroup.appliesTo != p6.storage.interfaces.IWork:
        return None
    return lambda x: MetadataPage(x, metaGroup)

def page_IWorkItem(metaGroup, appliesTo):
    """Subscription adapter to adapt a metadata group to a wizard page."""
    if metaGroup.appliesTo != p6.storage.interfaces.IWorkItem:
        return None
    return lambda x: ItemMetadataPage(x, metaGroup)

def generatePages(itemInterfaces=[p6.storage.interfaces.IWork,
                                  p6.storage.interfaces.IWorkItem]
                  ):
    """Returns a list of page objects, automatically generated from the
    supplied metadata field definitions."""

    pages = []
    for itemType in itemInterfaces:

        print 'finding for...', itemType
        for group in [n for n in p6.getApp().groups
                      if n.appliesTo == itemType]:

            print group
            # check for an adapter which will adapt our metadata group
            # to an IWizardPage; first check for an adapter that adapts the
            # group alone (ie, for a specialized group implementation), and
            # then check for dual adaptation (ie, for the more generic
            # implementation of our base metadata group class whose display
            # varies depending on what it "applies" to.

            page = zope.component.queryMultiAdapter(
                (group,),
                p6.ui.interfaces.IWizardPage) or \
                zope.component.queryMultiAdapter(
                (group,group),
                p6.ui.interfaces.IWizardPage)

            if page:
                pages.append(page)

    return pages
