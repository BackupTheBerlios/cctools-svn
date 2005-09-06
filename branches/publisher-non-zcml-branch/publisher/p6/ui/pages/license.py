"""LicenseChooser custom metadata wizard page."""

import webbrowser
import urllib2

import wx
import wx.html

import libxml2
import libxslt

import zope.interface
import zope.component

import ccwx.xrcwiz
import ccwsclient

import p6.ui
import p6.metadata

class WebbrowserHtml(wx.html.HtmlWindow):
    """Proxy class for L{wx.html.HtmlWindow} which opens a web browser
    when the user clicks a link."""
    
    def OnLinkClicked(self, linkinfo):
        """Respond to link click by opening a new window in the user's
        web browser."""
        
        webbrowser.open( linkinfo.GetHref(), True, True )

BGCOLOR = "efefef"

class LicenseChooserPage(ccwx.xrcwiz.XrcWizPage):
    """Custom wizard page which implements a license chooser based on
    CC's web service interface."""
    
    zope.interface.implements(p6.ui.interfaces.IWizardPage)

    def __init__(self, parent, metaGroup):
        ccwx.xrcwiz.XrcWizPage.__init__(self, parent,
                                        self.PAGE_XRC,
                                        'LICENSE_CHOOSER',
                                        'Choose A License')

        self.metagroup = metaGroup

        # initialize tracking attributes
        self._license_doc = None
        self.__license = ''
        self.__fields = []
        self.__fieldinfo = {}

        # create the web services proxy
        self.__cc_server = ccwsclient.CcRest(self.REST_ROOT)
        
        # create the sizer
        self.sizer = self.GetSizer()
        
        self.sizer.Add(wx.StaticText(parent=self,
                       label=self.STR_INTRO_TEXT),
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
                                                label='License Class:')
        
        wx.CallAfter(self.getLicenseClasses)

        self.fieldSizer.Add(self.lblLicenses)
        self.fieldSizer.Add(self.cmbLicenses, flag=wx.EXPAND)

        # set up the license URL widget
        self.txtLicense = WebbrowserHtml(self, -1)
        self.txtLicense.SetPage(self.HTML_LICENSE % (BGCOLOR, 'foo', 'foo'))
        ir = self.txtLicense.GetInternalRepresentation()
        self.txtLicense.SetSize( (ir.GetWidth()+25, ir.GetHeight()+25) )

        self.sizer.Add(self.txtLicense, flag=wx.EXPAND)
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
                         caption="ccPublisher: Error.",
                         style=wx.OK|wx.ICON_ERROR, parent=self.GetParent())
            self.GetParent().Close()

        self.cmbLicenses.AppendItems(self.__l_classes.values())
        self.cmbLicenses.SetValue('Creative Commons')
        
        try:
            self.onSelectLicenseClass(None)
            # XXX not needed... onselect calls this...
            # self.updateLicense(None)
        except:
            pass
        
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

        self._license_doc = self.__cc_server.issue(self.__license, answers)

        # XXX do some sort of field name matching here?
        # update the metadata field
        for field in self.metagroup.getFields():
            zope.component.handle(
                p6.metadata.events.UpdateMetadataEvent(self.metagroup.appliesTo,
                                                       field,
                                                       self.getLicenseUrl()
                                                       )
                )
                
    def getLicenseUrl(self):
        """Extract the license URL from the returned licensing document."""
        if self._license_doc is None:
            return None

        try:
            d = libxml2.parseMemory(self._license_doc, len(self._license_doc))
            c = d.xpathNewContext()

            uri = c.xpathEval('//result/license-uri')[0].content
        except libxml2.parserError:
            return None

        return uri

    def getLicenseName(self):
        """Extract the license name from the returned licensing document."""
        if self._license_doc is None:
            return None

        try:
            d = libxml2.parseMemory(self._license_doc, len(self._license_doc))
            c = d.xpathNewContext()

            uri = c.xpathEval('//result/license-name')[0].content
        except libxml2.parserError:
            return None

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
                self.__fieldinfo[field]['control'] = \
                     wx.ComboBox(self.pnlFields,
                                 style=wx.CB_DROPDOWN|wx.CB_READONLY,
                                 choices = self.__fieldinfo[field]['enum'].values()
                                 )

                self.__fieldinfo[field]['control'].SetToolTip(
                    wx.ToolTip(self.__fieldinfo[field]['description']))
                self.__fieldinfo[field]['control'].SetSelection(0)
                self.Bind(wx.EVT_COMBOBOX, self.updateLicense,
                          self.__fieldinfo[field]['control'])
                self.Bind(wx.EVT_TEXT, self.updateLicense,
                          self.__fieldinfo[field]['control'])
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
        self.txtLicense.SetPage(self.HTML_LICENSE % (BGCOLOR, self.getLicenseUrl(), self.getLicenseName()))
        # "You chose %s" % str(self.getLicenseName()))
                    
    def validate(self, event):
        return True

    REST_ROOT = 'http://api.creativecommons.org/rest'
    STR_INTRO_TEXT="""With a Creative Commons license, you keep your copyright but allow people to copy and distribute your work provided the give you credit -- and only on the conditions you specify here.  If you want to offer your work with no conditions, choose the Public Domain."""

    HTML_LICENSE = '<html><body bgcolor="#%s"><font size="3">You chose <a href="%s">%s</a>.</font></body></html>'

    PAGE_XRC = """
<resource>
  <object class="wxPanel" name="LICENSE_CHOOSER">
    <object class="wxFlexGridSizer">
      <cols>1</cols>
      <vgap>5</vgap>
      <hgap>5</hgap>
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


