"""LicenseChooser custom metadata wizard page."""

import urllib2
import thread

import wx
import wx.lib.hyperlink

import elementtree.ElementTree as etree

import zope.interface
import zope.component

import ccwx.xrcwiz
import ccwsclient

import p6.api
import p6.ui
import p6.metadata
import p6.app.support.browser as webbrowser

from p6.i18n import _

class LicenseChooserPage(ccwx.xrcwiz.XrcWizPage):
    """Custom wizard page which implements a license chooser based on
    CC's web service interface."""
    
    zope.interface.implements(p6.ui.interfaces.IWizardPage)

    def __init__(self, parent, metaGroup):
        ccwx.xrcwiz.XrcWizPage.__init__(self, parent,
                                        self.PAGE_XRC,
                                        'LICENSE_CHOOSER',
                                        _('Choose A License'))

        self.metagroup = metaGroup

        # initialize tracking attributes
        self._license_doc = None
        self.__license = ''
        self.__fields = []
        self.__fieldinfo = {}

        # initialize tracking for work information
        self.__workinfo = {}
        
        # create the web services proxy
        self.__cc_server = ccwsclient.CcRest(self.REST_ROOT,
                                             lang=p6.i18n.getLocale())
        
        # create the sizer
        self.sizer = self.GetSizer()
        
        self.sizer.Add(wx.StaticText(parent=self,
                       label=_(self.STR_INTRO_TEXT)),
                       flag=wx.EXPAND)

        # create the panel for the fields
        self.pnlFields = wx.Panel(self)
        self.sizer.Add(self.pnlFields, flag=wx.EXPAND)

        # set up the field panel sizer
        self.fieldSizer = wx.FlexGridSizer(0, 2, 5, 5)
        self.fieldSizer.AddGrowableCol(1)
        self.pnlFields.SetSizer(self.fieldSizer)

        # create the basic widgets
        self.cmbLicenses = wx.ComboBox(self.pnlFields,
                                       style=wx.CB_DROPDOWN|wx.CB_READONLY
                                       )
        self.lblLicenses = wx.StaticText(parent=self.pnlFields,
                                         label=_('License Class:'))

        # retrieve the license classes in a background thread
        #thread.start_new_thread(self.getLicenseClasses, ())
        self.getLicenseClasses()

        self.fieldSizer.Add(self.lblLicenses)
        self.fieldSizer.Add(self.cmbLicenses, flag=wx.EXPAND)

        # create the license deed hyperlink
        deed_sizer = wx.BoxSizer(wx.HORIZONTAL)
        deed_sizer.Add( wx.StaticText(self, -1, _("Selected License:")) )
        deed_sizer.Add( (10, 10) )
        
        self.lblLicense = wx.lib.hyperlink.HyperLinkCtrl(
            self, wx.ID_ANY, _("None selected"), URL="")
        deed_sizer.Add(self.lblLicense)

        self.sizer.Add(deed_sizer, flag=wx.EXPAND)
        #self.sizer.Add(self.lblLicense)

        # update the layout
        self.Layout()

        # bind event handlers
        self.Bind(wx.EVT_COMBOBOX, self.onSelectLicenseClass, self.cmbLicenses)

        self.Hide()

    def getLicenseClasses(self):
        """Calls the SOAP API via proxy to get a list of all available
        license class identifiers."""

        try:
            self.__l_classes = self.__cc_server.license_classes()
        except urllib2.URLError, e:
            wx.MessageBox("Unable to connect to the Internet to retrieve license information.  Check your connection and try again.",
                         caption=_("appname") + ": " + _("Error"),
                         style=wx.OK|wx.ICON_ERROR, parent=self.GetParent())
            self.GetParent().Close()
            return

        # update the list of license classes
        self.cmbLicenses.AppendItems(self.__l_classes.values())
        
        # default to the "standard" license class
        self.cmbLicenses.SetValue(self.__l_classes['standard'])

        # use wx.CallAfter to schedule the call (can't touch GUI in a thread)
        wx.CallAfter(lambda: self.onSelectLicenseClass(None))
        
    def onLicense(self, event):
        """Submit selections and display license info."""
        answers = {}

        for field in self.__fields:
            if self.__fieldinfo[field]['type'] == 'enum':
                answer_list = [n for n in self.__fieldinfo[field]['enum'] if
                              self.__fieldinfo[field]['enum'][n] ==
                              self.__fieldinfo[field]['control'].GetValue()]
                if len(answer_list) > 0:
                    answer_key = answer_list[0]
                else:
                    return

                answers[field] = answer_key 

        self._license_doc = self.__cc_server.issue(self.__license, answers,
                                                   workinfo=self.__workinfo)

        # XXX do some sort of field name matching here?
        # update the metadata field
        for field in self.metagroup.getFields():
            zope.component.handle(
                p6.metadata.events.UpdateMetadataEvent(
                      self.metagroup.appliesTo,
                      field,
                      self.getLicenseUrl()
                                                       )
                )

        # XXX hack: store the license document on the app object
        p6.api.getApp().license_doc = self._license_doc
                
    def getLicenseUrl(self):
        """Extract the license URL from the returned licensing document."""
        if not(self._license_doc):
            return None

        d = etree.fromstring(self._license_doc)
        uri = d.find('license-uri').text

        return uri

    def getLicenseName(self):
        """Extract the license name from the returned licensing document."""
        if not(self._license_doc):
            return None

        d = etree.fromstring(self._license_doc)
        uri = d.find('license-name').text

        return uri
    
    def clearChooser(self):
        # delete everything except the license class chooser and label
        for child in self.pnlFields.GetChildren():
            if child != self.lblLicenses and child != self.cmbLicenses:
                child.Destroy()

        del self.__fieldinfo
        self.__fieldinfo = {}
        
    def onSelectLicenseClass(self, event):
        if event is not None and (
           event.GetString() == '' or \
           event.GetString() == self.__license):
            # bail out if there's no change; we'll get called again momentarily
            return

        if event is not None:
            license_str = event.GetString()
        else:
            license_str = self.cmbLicenses.GetValue()
            
        # get the new license ID
        self.__license = [n for n in self.__l_classes.keys()
                          if self.__l_classes[n] == license_str][0]
        
        # clear the sizer
        self.clearChooser()

        # retrieve the fields
        fields = self.__cc_server.fields(self.__license)
        self.__fields = fields['__keys__']
        self.__fieldinfo = fields

        for field in self.__fields:
            # update the UI
            self.updateFieldDetails(field)

        self.updateLicense(event)
        self.Layout()

    def updateFieldDetails(self, fieldid):
        
        field = fieldid

        self.__fieldinfo[field] = dict(self.__fieldinfo[field])

        # make sure we have a label
        if self.__fieldinfo[field]['label'] == '':
            self.__fieldinfo[field]['label'] = field

        # add the label text
        self.__fieldinfo[field]['label_ctrl'] = wx.StaticText(
            self.pnlFields,
            label=self.__fieldinfo[field]['label'])

        self.pnlFields.GetSizer().Add(self.__fieldinfo[field]['label_ctrl'])
        # add the control
        if self.__fieldinfo[field]['type'] == 'enum':
            # enumeration field; determine if we're using a combo or radio btns
            if len(self.__fieldinfo[field]['enum'].values()) > 3:
                # using a combo box

                # get the list of values; store the first one, we'll use
                # it as the default
                choices = self.__fieldinfo[field]['enum'].values()
                default = choices[0]

                # sort the list of options
                choices.sort()

                # create the widget
                self.__fieldinfo[field]['control'] = \
                     wx.ComboBox(self.pnlFields,
                                 style=wx.CB_DROPDOWN|wx.CB_READONLY,
                                 choices = choices
                                 )

                # set tool tips, event handlers, default...
                self.__fieldinfo[field]['control'].SetToolTip(
                    wx.ToolTip(self.__fieldinfo[field]['description']))
                self.Bind(wx.EVT_COMBOBOX, self.updateLicense,
                          self.__fieldinfo[field]['control'])
                self.Bind(wx.EVT_TEXT, self.updateLicense,
                          self.__fieldinfo[field]['control'])

                self.__fieldinfo[field]['control'].SetSelection(
                    self.__fieldinfo[field]['control'].FindString(default)
                    )
            else:
                # using radio buttons
                self.__fieldinfo[field]['control'] = wx.BoxSizer(wx.VERTICAL)
                
                # create the choice radio buttons
                first = True
                for e in self.__fieldinfo[field]['enum'].values():
                    if first:
                        rb = wx.RadioButton(self.pnlFields, -1, label=e,
                                            style=wx.RB_GROUP)
                        rb.SetValue(True)
                        first = False
                    else:
                        rb = wx.RadioButton(self.pnlFields, -1, label=e)

                    rb.SetToolTip(
                        wx.ToolTip(self.__fieldinfo[field]['description']))
                        
                    self.__fieldinfo[field]['control'].Add(rb)
                    self.Bind(wx.EVT_RADIOBUTTON, self.updateLicense, rb)

                # inject the GetValue method
                self.__fieldinfo[field]['control'].GetValue = \
                    lambda :self.GetCBValue(self.__fieldinfo[field]['control'])

            self.pnlFields.GetSizer().Add(
                self.__fieldinfo[field]['control'], flag=wx.EXPAND)

    def GetCBValue(self, radioSizer):
        for item in radioSizer.GetChildren():
            if item.GetWindow().GetValue():
                return item.GetWindow().GetLabel()
            
        return None
    
    def updateLicense(self, event):
        self.onLicense(event)
        
        self.lblLicense.SetLabel(self.getLicenseName())
        self.lblLicense.SetURL(self.getLicenseUrl())
        self.lblLicense.SetToolTip(wx.ToolTip(self.getLicenseUrl()))
        
        self.lblLicense.UpdateLink()
                    
    def validate(self, event):
        return True

    def onChanged(self, event):

        # update the work information
        self.__workinfo =p6.api.workInformation()

        # force another call to the web service to incorporate any work info
        self.onLicense(None)
        
    REST_ROOT = 'http://api.creativecommons.org/rest/dev'
    STR_INTRO_TEXT="""With a Creative Commons license, you keep your copyright but allow people to copy and distribute your work provided the give you credit -- and only on the conditions you specify here.  If you want to offer your work with no conditions, choose the Public Domain."""

    PAGE_XRC = """
<resource>
  <object class="wxPanel" name="LICENSE_CHOOSER">
    <object class="wxFlexGridSizer">
      <cols>1</cols>
      <vgap>2</vgap>
      <growablecols>0</growablecols>
      <growablerows>1,2</growablerows>
    </object>
  </object>
</resource>
    """

def page_ILicenseGroup(metaGroup):
    """Adapter from L{p6.metadata.license.ILicenseGroup} to
    L{p6.ui.interfaces.IWizardPage}.
    """
    return lambda x: LicenseChooserPage(x, metaGroup)


