import weakref

import wx
import ccwx

import zope.component
import zope.interface

import p6
import p6.api

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

        # see if we have a description; if so, use it to label the page
        if metaGroup.description:
            desc_label = wx.StaticText(self, label=metaGroup.description)
            self.GetSizer().Add(desc_label, flag=wx.EXPAND)

        # create the actual sizer to hold the labels and widgets
        item_sizer = wx.FlexGridSizer(cols=2)
        item_sizer.AddGrowableCol(1)
        self.GetSizer().Add(item_sizer, flag=wx.EXPAND)

        self.addFields(metaGroup, item_sizer)

    def addFields(self, metaGroup, sizer):
        """Create the user input widgets for this group."""

        for field in metaGroup.getFields():

            label = wx.StaticText(self, label=field.label)
            sizer.Add(label)

            widget = p6.ui.interfaces.IEntryWidget(field)(self)
            field._widget = weakref.ref(widget)
            
            sizer.Add(widget, flag=wx.EXPAND)

            # check for a tooltip
            if field.tip:
                widget.SetToolTip(wx.ToolTip(field.tip))

            # check for a description
            if field.description:
                sizer.Add((5,5))
                desc_label = wx.StaticText(self, label=field.description)
                sizer.Add(desc_label, flag=wx.EXPAND)

    def onValidate(self, event):
        errors = []

        # validate the metadata
        for field in self.metagroup.getFields():
            widget = field._widget()

            if widget is not None:
                v_result = field.validator(widget.GetValue())
                
                if v_result is not None:
                    errors.append(v_result)

        if len(errors) > 0:
            # display the error messages
            wx.MessageDialog(None, "\n".join(errors),
                             style=wx.ICON_ERROR|wx.OK).ShowModal()
            
            # veto the event
            event.Veto()
            return
        
    def onChanging(self, event):
        """Perform storage of field values back to metadata framework."""

        if event.direction:
            self.onValidate(event)
            
        for field in self.metagroup.getFields():
            widget = field._widget()

            if widget is not None:
                zope.component.handle(
                    p6.metadata.events.UpdateMetadataEvent(self.metagroup.appliesTo,
                                                           field.id,
                                                           widget.GetValue()
                                                           )
                    )
                
        
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
                p6.api.deinstify(self.onItemSelected))
            )
        
        # bind wx events
        self.Bind(ccwx.xrcwiz.EVT_XRCWIZ_PAGE_CHANGED, self.onChanged)

    def onItemSelected(self, event):
        self.__items.append(event.item)

    def onItemDeselected(self, event):
        del self.__items[self.__items.index(event.item)]

    def initFields(self, metaGroup):
        """Create the user input widgets for this group."""

        # see if we have a description; if so, use it to label the page
        if metaGroup.description:
            desc_label = wx.StaticText(self, label=metaGroup.description)
            self.GetSizer().Add(desc_label, flag=wx.EXPAND)

        # reset widget references
        for field in metaGroup.getFields():
            field._widget = {}

        # create the widgets for each item
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
                widget = field._widget[item]()

                if widget is not None:
                    zope.component.handle(
                        p6.metadata.events.UpdateMetadataEvent(item,
                                                               field.id,
                                                             widget.GetValue()
                                                               )
                        )


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

def work_metaGroupWizPage(metaGroup):
    """Subscription adapter to adapt a metadata group to a wizard page."""
    if metaGroup.appliesTo == p6.storage.interfaces.IWork:
        return lambda x: MetadataPage(x, metaGroup)
    else:
        return None

def item_metaGroupWizPage(metaGroup):
    """Subscription adapter to adapt a metadata group to a wizard page."""
    
    if metaGroup.appliesTo == p6.storage.interfaces.IWorkItem:
        return lambda x: ItemMetadataPage(x, metaGroup)
    else:
        return None

def storage_metaGroupWizPage(metaGroup):
    """Subscription adapter to adapt a metadata group to a wizard page."""
    if metaGroup.appliesTo == p6.storage.interfaces.IStorage:
        return lambda x: MetadataPage(x, metaGroup)
    else:
        return None

def generatePages(itemInterfaces=[p6.storage.interfaces.IWork,
                                  p6.storage.interfaces.IWorkItem,
                                  p6.storage.interfaces.IStorage]
                  ):
    """Returns a list of page objects, automatically generated from the
    supplied metadata field definitions."""

    pages = []
    for itemType in itemInterfaces:

        print 'finding for...', itemType
        for group in [n for n in p6.api.getApp().groups
                      if n.appliesTo == itemType]:

            # check for an adapter which will adapt our metadata group
            # to an IWizardPage; first check for an adapter that adapts the
            # group alone (ie, for a specialized group implementation), and
            # then check for dual adaptation (ie, for the more generic
            # implementation of our base metadata group class whose display
            # varies depending on what it "applies" to.

            page = zope.component.getGlobalSiteManager().getAdapters(
                (group,),
                p6.ui.interfaces.IWizardPage)

            if page:
                pages.append(page[0][1])

    return pages
