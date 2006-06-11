"""Standard metadata page."""

import weakref

import wx
import ccwx

import zope.component
import zope.interface

import p6
import p6.api
import p6.extension.exceptions

import license

from p6.i18n import _

class SimpleFieldPage(ccwx.xrcwiz.XrcWizPage):
    """Utility page for rendering a set of MetadataField objects independtly
    of a MetadataGroup.  Intended to be used for collecting information from
    the user in a way that is consistent with the rest of the UI, but which
    doesn't necessarily apply to the work they are uploading."""
    
    zope.interface.implements(p6.ui.interfaces.IWizardPage)

    def __init__(self, parent, id, headline, fields, validator,
                 description=""):
        """Fields is a sequence of metadata fields."""
        
        ccwx.xrcwiz.XrcWizPage.__init__(self, parent,
                                        self.PAGE_XRC % id,
                                        id,
                                        headline)

        self.__fields = fields
        self.__description = description
        self.__validator = validator
        
        self.initFields(fields)

    def initFields(self, fields):
        """Create the user input widgets for this group."""

        # add any description text
        self.GetSizer().Add(wx.StaticText(self, -1, _(self.__description)))
            
        # create the actual sizer to hold the labels and widgets
        item_sizer = wx.FlexGridSizer(cols=2)
        item_sizer.AddGrowableCol(1)
        self.GetSizer().Add(item_sizer, flag=wx.EXPAND)

        self.addFields(fields, item_sizer)

    def addFields(self, field_list, sizer):
        """Create the user input widgets for this group."""

        for field in field_list:

            label = wx.StaticText(self, label=_(field.label))
            sizer.Add(label)

            widget = p6.ui.interfaces.IEntryWidget(field)(self)
            widget.SetValue(field.default)
            
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


    def __assemble(self):
        """Return a dictionary containing id-value pairs for
        the metadata fields."""

        result = {}
        
        for f in self.__fields:
            result[f.id] = f._widget().GetValue()

        return result
        
    def onChanging(self, event):
        try:
            if event.direction:
                return self.__validator(self.__assemble())
            else:
                return True
        except p6.extension.exceptions.ExtensionSettingsException, e:
            # an error occured while validating the extension settings
            # show an alert
            wx.MessageDialog(None, _(str(e)), _("Error"), wx.OK).ShowModal()
            
            # veto the event -- don't allow the page to change w/o correction
            event.Veto()

    PAGE_XRC = """
<resource>
  <object class="wxPanel" name="%s">
    <object class="wxFlexGridSizer">
      <cols>1</cols>
      <vgap>5</vgap>
      <hgap>5</hgap>
      <growablecols>0</growablecols>
      <growablerows>1</growablerows>
    </object>
  </object>
</resource>
    """
