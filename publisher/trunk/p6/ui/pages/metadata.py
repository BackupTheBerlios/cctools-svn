"""Standard metadata page."""

import weakref

import wx

import zope.component
import zope.interface

import p6
import p6.api
import p6.ui.wizard

import license

import inspect

from p6.i18n import _
from p6.ui.interfaces import ILabelText

class MetadataPage(p6.ui.wizard.XRCWizardPage):
    """Basic metadata page; generated for most metadata groups."""
    zope.interface.implements(p6.ui.interfaces.IWizardPage)

    def __init__(self, parent, metaGroup):
        p6.ui.wizard.XRCWizardPage.__init__(self, parent, _(metaGroup.title),
                                        self.PAGE_XRC % metaGroup.id,
                                        metaGroup.id
                                        )

        self.metagroup = metaGroup
        self.initFields(metaGroup)

    def initFields(self, metaGroup):
        """Create the user input widgets for this group."""

        # see if we have a description; if so, use it to label the page
        if metaGroup.description:
            desc_label = wx.StaticText(self, label=_(metaGroup.description))
            self.GetSizer().Add(desc_label, flag=wx.EXPAND)

        # create the actual sizer to hold the labels and widgets
        item_sizer = wx.FlexGridSizer(cols=2)
        item_sizer.AddGrowableCol(1)
        self.GetSizer().Add(item_sizer, flag=wx.EXPAND)

        # register our generic update handler
        zope.component.provideHandler(
            zope.component.adapter(p6.metadata.events.IUpdateMetadataEvent)(
                p6.api.deinstify(self.updateField))
            )

        self.addFields(metaGroup, item_sizer)

    def updateField(self, event):
        """Generic IUpdateMetadataEvent handler that keeps the UI in sync."""
        if self.metagroup == event.field.group():
            event.field._widget().SetValue(event.value)
        
    def addFields(self, metaGroup, sizer):
        """Create the user input widgets for this group."""

        for field in metaGroup.getFields():

            label = wx.StaticText(self, label=_(field.label))
            sizer.Add(label)

            widget = p6.ui.interfaces.IEntryWidget(field)(self)
            field._widget = weakref.ref(widget)
            
            sizer.Add(widget, flag=wx.EXPAND)

            # check for a tooltip
            if field.tip:
                widget.SetToolTip(wx.ToolTip(_(field.tip)))

            # check for a description
            if field.description:
                sizer.Add((5,5))
                desc_label = wx.StaticText(self, label=_(field.description))
                sizer.Add(desc_label, flag=wx.EXPAND)

            # check if the field is persistant and try to load it
            if field.persist:

                persistUtility = zope.component.getUtility(
                    p6.metadata.persistance.IMetadataPersistance)
                
                value = persistUtility.query(self.metagroup.id,
                                             field.id)

                # see if we have a value for this field
                if value is not None:
                    widget.SetValue(value)

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
                                                           field,
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

class ItemMetadataPage(p6.ui.wizard.XRCWizardPage):
    """Basic metadata page for groups which apply to an IItem interface;
    this page duplicates the fields as necessary in order to show the group
    for each item the group applies to."""
    
    zope.interface.implements(p6.ui.interfaces.IWizardPage)

    def __init__(self, parent, metaGroup):
        p6.ui.wizard.XRCWizardPage.__init__(self, parent,
                                        metaGroup.title,
                                        self.PAGE_XRC % metaGroup.id,
                                        metaGroup.id)

        self.metagroup = metaGroup
        self.__items = []
        self.initFields(self.metagroup)

        # bind P6 events
        zope.component.provideHandler(
            zope.component.adapter(p6.storage.events.IItemSelected)(
                p6.api.deinstify(self.onItemSelected))
            )
        
        zope.component.provideHandler(
            zope.component.adapter(p6.storage.events.IItemDeselected)(
                p6.api.deinstify(self.onItemDeselected))
            )
        
        # bind wx events
        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, self.onChanged)

    def onItemSelected(self, event):
        # check if this event's item should be stored here...
        if (self.metagroup.appliesTo in
            zope.interface.providedBy(event.item)):

            self.__items.append(event.item)

    def onItemDeselected(self, event):
        # check if this event's item should be stored here...
        if (self.metagroup.appliesTo in
            zope.interface.implementedBy(event.item.__class__)):

            self.__items.remove(event.item)
            #del self.__items[self.__items.index(event.item)]

    def initFields(self, metaGroup):
        """Create the user input widgets for this group."""

        # clear the sizer
        self.GetSizer().Clear()
        
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
            item_label = wx.StaticText(self,
                                       label=ILabelText(item).text)
            self.GetSizer().Add(item_label, flag=wx.EXPAND)

            # create the item sizer
            item_sizer = wx.FlexGridSizer(cols=2)
            item_sizer.AddGrowableCol(1)
            self.GetSizer().Add(item_sizer, flag=wx.EXPAND)
            
            for field in metaGroup.getFields():

                label = wx.StaticText(self, label=_(field.label))
                item_sizer.Add(label)

                widget = p6.ui.interfaces.IEntryWidget(field)(self)
                
                value = p6.metadata.interfaces.IMetadataStorage(item).\
                        getMetaValue(field.id, default='')
                widget.SetValue(value)

                field._widget[item] = weakref.ref(widget)
                item_sizer.Add(widget, flag=wx.EXPAND)

    def onValidate(self, event):
        errors = []

        # validate the metadata
        for field in self.metagroup.getFields():

            # check the widget for each item displayed
            for widget in field._widget:

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

        for item in self.__items:
            for field in self.metagroup.getFields():
                widget = field._widget[item]()

                if widget is not None:
                    zope.component.handle(
                        p6.metadata.events.UpdateMetadataEvent(item,
                                                               field,
                                                             widget.GetValue()
                                                               )
                        )


    def onChanged(self, event):
        if event.direction:
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
    """Subscription adapter to adapt a metadata group which applies to
    L{p6.storage.interfaces.IWork} to a wizard page.

    If you define your own item type, you need to register an adapter from
    the type's interface to L{p6.ui.interfaces.IWizardPage}.
    """
    if metaGroup.appliesTo == p6.storage.interfaces.IWork:
        return lambda x: MetadataPage(x, metaGroup)
    else:
        return None

def item_metaGroupWizPage(metaGroup):
    """Subscription adapter to adapt a metadata group which applies to
    L{p6.storage.interfaces.IWorkItem} to a wizard page.

    If you define your own item type, you need to register an adapter from
    the type's interface to L{p6.ui.interfaces.IWizardPage}.
    """
    
    if metaGroup.appliesTo == p6.storage.interfaces.IWorkItem:
        return lambda x: ItemMetadataPage(x, metaGroup)
    else:
        return None

def storage_metaGroupWizPage(metaGroup):
    """Subscription adapter to adapt a metadata group which applies to
    L{p6.storage.interfaces.IStorage} to a wizard page.\

    If you define your own item type, you need to register an adapter from
    the type's interface to L{p6.ui.interfaces.IWizardPage}.
    """
    
    if metaGroup.appliesTo == p6.storage.interfaces.IStorage:
        return lambda x: MetadataPage(x, metaGroup)
    else:
        return None

def generatePages(itemInterfaces=[p6.storage.interfaces.IWork,
                                  p6.storage.interfaces.IWorkItem,
                                  p6.storage.interfaces.IStorage]
                  ):
    """Returns a list of page objects, automatically generated from the
    supplied metadata field definitions.

    @param itemInterfaces: Interfaces to generate pages for.
    @type  itemInterfaces: sequence
    """

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
