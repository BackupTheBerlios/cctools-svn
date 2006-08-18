"""ccPublisher-specific user interface components."""

import os
import socket
import re
import elementtree.ElementTree as etree

import wx
import wx.html
import wx.lib.hyperlink
from wx.xrc import XRCCTRL

import ccwx
import zope.interface

import p6
import p6.api
import p6.ui.pages.fieldrender
from p6.i18n import _

import pycchost


class CCHostLocationPage(p6.ui.pages.fieldrender.SimpleFieldPage):
    def __init__(self, parent, storage):
        url = p6.metadata.persistance.load("cch", "url", "")

        fields = [
            p6.metadata.base.metadatafield(p6.metadata.types.ITextField)(
            'url', 'CCHost Installation URL', default=url)
            ]
        description=_("Enter CCHost Installation's URL. For example: http://www.ccmixter.org/")

        p6.ui.pages.fieldrender.SimpleFieldPage.__init__(self,
                                                         parent,
                                                         'CCHost_LOCATION',
                                                   _('CCHost Installation URL'),
                                                         fields,
                                                         self.callback,
                                                         description)
        self.storage = storage

    def callback(self, value_dict):
        
        # make url was provided
        if not('url' in value_dict):
            raise p6.extension.exceptions.ExtensionSettingsException(
                "You must supply an URL.")

	theurl = value_dict['url']
        if theurl[len(theurl)-1] != '/':
            theurl = theurl + "/"
        # verify if the url is a valid ccHost Installation and find it's name
        try:
	    if not(pycchost.location.validate(theurl, self.storage.Request, self.storage.urlopen)):
                raise p6.extension.exceptions.ExtensionSettingsException(
                    _("Invalid URL."))
	    title = pycchost.location.title(theurl, self.storage.Request, self.storage.urlopen)
	        
	except IOError, e:
	    if hasattr(e, 'reason'):
	        raise p6.extension.exceptions.ExtensionSettingsException(
                    _("Failed to open the URL.\nThe error reason: %s.\nThis usually means the server doesn't exist, is down, or we don't have an internet connection." % e.reason))
	    else:
		raise p6.extension.exceptions.ExtensionSettingsException(
                    _("Failed to open the URL. This usually means the server doesn't exist, is down, or we don't have an internet connection."))

        # store the valid url
        self.storage.location = theurl
	# get ccHost installation name
	self.storage.title = title
        p6.metadata.persistance.store("cch", "url", theurl)
        

class CCHostLoginPage(p6.ui.pages.fieldrender.SimpleFieldPage):

    def __init__(self, parent, storage):
        # check if we have persisted values for username/passwd
        username = p6.metadata.persistance.load("cch", "username", "")
        password = p6.metadata.persistance.load("cch", "password", "")
        persist  = p6.metadata.persistance.load("cch", "persist", False)

        # create the simple page
        fields = [
            p6.metadata.base.metadatafield(p6.metadata.types.ITextField)(
            'username', 'Username', default=username),
            p6.metadata.base.metadatafield(p6.metadata.types.IPasswordField)(
            'password', 'Password', default=password),
            p6.metadata.base.metadatafield(p6.metadata.types.IBooleanField)(
            'persist', 'Save your username and password?', default=persist)
            ]

        description=_("Enter your CCHost Installation username and password.")

        p6.ui.pages.fieldrender.SimpleFieldPage.__init__(self,
                                                         parent,
                                                         'CCHost_LOGIN',
                                                   _('CCHost Installation login'),
                                                         fields,
                                                         self.callback,
                                                         description)
        self.storage = storage


    def callback(self, value_dict):

        # make sure both a username and password were provided
        if not('username' in value_dict and 'password' in value_dict):
            raise p6.extension.exceptions.ExtensionSettingsException(
                "You must supply both a username and password.")

        # validate the credentials with ccHost Installation
        try:
            if not(pycchost.user.validate(value_dict['username'],
                                           value_dict['password'], self.storage.location, self.storage.Request, self.storage.urlopen)):

                raise p6.extension.exceptions.ExtensionSettingsException(
                    _("Invalid username or password."))
        except IOError, e:
	    if hasattr(e, 'reason'):
	        raise p6.extension.exceptions.ExtensionSettingsException(
                    _("Failed to open the URL.\nThe error reason: %s.\nThis usually means the server doesn't exist, is down, or we don't have an internet connection." % e.reason))
	    else:
		raise p6.extension.exceptions.ExtensionSettingsException(
                    _("Failed to open the URL. This usually means the server doesn't exist, is down, or we don't have an internet connection."))

        # store the credentials for future use
        self.storage.credentials = (value_dict['username'],
                                    value_dict['password'])
        # check if the user wanted to persist them
        if value_dict['persist']:
            # store them
            p6.metadata.persistance.store("cch", "username", value_dict['username'])
            p6.metadata.persistance.store("cch", "password", value_dict['password'])
            p6.metadata.persistance.store("cch", "persist", True)
        else:
            # clear the potentially persisted values
            p6.metadata.persistance.store("cch", "username", "")
            p6.metadata.persistance.store("cch", "password", "")
            p6.metadata.persistance.store("cch", "persist", False)


        # register for future storage events after validating our
        # storage-specific settings

        self.storage.registerEvents()

class CCHostSubmissionTypePage(ccwx.xrcwiz.XrcWizPage):
	"""User interface page which displays a list of available
	submission types and allows the user to select one or more.
	"""
	zope.interface.implements(p6.ui.interfaces.IWizardPage)

	def __init__(self, parent, storage, headline=_('Pick Up Submission Type')):
		"""
	        @param parent: Parent window
	        @type parent: L{wx.Window}
	
	        @param headline: Title to display above the wizard page
	        @type headline: String
	        """

	        ccwx.xrcwiz.XrcWizPage.__init__(self, parent,
                	                        self.PAGE_XRC, self.XRCID, headline)

        	self.storage = storage

	def init(self):

		self.__options = []
		self.GetSizer().Clear(True)
		self.Fit()

		#get a list of submission types and their links
		try:
			list =  pycchost.type.getSubmissionTypes(self.storage.location, self.storage.Request, self.storage.urlopen)
		except IOError, e:
			list = []
	    		if hasattr(e, 'reason'):
	        	    raise p6.extension.exceptions.ExtensionSettingsException(
	                        _("Failed to open the URL.\nThe error reason: %s.\nThis usually means the server doesn't exist, is down, or we don't have an internet connection." % e.reason))
	    		else:
			    raise p6.extension.exceptions.ExtensionSettingsException(
                    		_("Failed to open the URL. This usually means the server doesn't exist, is down, or we don't have an internet connection."))
		else:
			self.list = list

		for op in range(len(list)):
                        if (op % 2 == 1):
				# set the first item to wx.RB_GROUP to make them mutually exclusive
				if op == 1:
					style = wx.RB_GROUP
				else:
					style = 0

				# create the new radio button
				rdbItem = wx.RadioButton(self, label=list[op], style=style)
				rdbItem.id = (op/2)+1
				self.__options.append(rdbItem)
				self.GetSizer().Add(rdbItem)
		self.Fit()

	def onChanged(self, event):
	        if event.direction:
        		self.init()

	def onChanging(self, event):
		for rdbOption in self.__options:
			if rdbOption.GetValue():
				# this option is selected
				self.storage.submissiontype = self.list[2*rdbOption.id-1]
				self.storage.submissionlink = self.list[2*(rdbOption.id-1)]

		# register for future storage events after validating our
	        # storage-specific settings
	        self.storage.registerEvents()		

	XRCID = "SUBMISSION_TYPE_SELECTOR"
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

class CCHostFormSubmission(ccwx.xrcwiz.XrcWizPage):
	"""User interface page which displays a form to
	submit files to a ccHost Installation
	"""		

	zope.interface.implements(p6.ui.interfaces.IWizardPage)

	def __init__(self, parent, storage, headline=_('Fill Submission Form')):
		"""
	        @param parent: Parent window
	        @type parent: L{wx.Window}
	
	        @param headline: Title to display above the wizard page
	        @type headline: String
	        """

	        ccwx.xrcwiz.XrcWizPage.__init__(self, parent,
                	                        self.PAGE_XRC, self.XRCID, headline)

		# creates an scrolled window
		self.sw = wx.ScrolledWindow(self)
		self.GetSizer().Add(self.sw, flag=wx.EXPAND)
		self.sw.SetSizer(wx.GridBagSizer(vgap=3, hgap=3))
		self.sizer = self.sw.GetSizer()
		self.sw.SetScrollbars(5, 5, 100, 100)

        	self.storage = storage

	def init(self, values=None):
		self.sizer.Clear(True)
		self.sw.Fit()
		self.sizer.AddGrowableCol(0)
		self.sizer.AddGrowableCol(1)
		row = 0

		#get a list of requested submission information
		try:
			form =  pycchost.form.getForm(self.storage.submissionlink, self.storage.Request, self.storage.urlopen, values)
		except IOError, e:
			form= []
	    		if hasattr(e, 'reason'):
	        	    raise p6.extension.exceptions.ExtensionSettingsException(
	                        _("Failed to open the URL.\nThe error reason: %s.\nThis usually means the server doesn't exist, is down, or we don't have an internet connection." % e.reason))
	    		else:
			    raise p6.extension.exceptions.ExtensionSettingsException(
                    		_("Failed to open the URL. This usually means the server doesn't exist, is down, or we don't have an internet connection."))
		else:
			self.form = form

		self.values = [] # list of submission fields
		self.list = [] # list of all form items and their names
		self.accept_remixes = False
		self.isRemix = False

		for inf in form:
			if not(inf.has_key("name")):
				inf['name'] = ""
			if not(inf.has_key("label")):
				inf['label'] = pycchost.form.getString(inf['name'])

			# get hidden form items values
			if inf['type'] == "hidden":
			        self.values.append((inf['name'], inf['value'][0]))
		
			# display form items
			elif inf['type'] == "submit":
				if inf['name'] == "search":
					formItem = wx.Button(self.sw, 1, inf['value'][0])
					self.sw.Bind(wx.EVT_BUTTON, self.search, id=1)
					self.sizer.Add(formItem, (row, 1), wx.DefaultSpan, wx.ALIGN_RIGHT)
					row += 1
				elif inf['name'] == "accept_remixes":
					formItem = wx.Button(self.sw, 2, inf['value'][0])
					self.sw.Bind(wx.EVT_BUTTON, self.accept, id=2)
					self.sizer.Add(formItem, (row, 1), wx.DefaultSpan,wx.ALIGN_RIGHT)
					row += 1
					self.accept_remixes = True
				else:
					self.values.append((inf['name'], inf['value'][0]))

			elif inf['type'] == "checkbox":
				formItem = wx.CheckBox(self.sw, label=inf['label'])
				if inf.has_key("value") and len(inf['value']) > 0 and inf['value'][0] == "checked":
					formItem.SetValue(True)
				else: 
					formItem.SetValue(False)
				if inf.has_key("tip"):
					formItem.SetToolTip(wx.ToolTip(inf['tip']))
				self.sizer.Add(formItem, (row, 0), (1,2), wx.EXPAND)
				row += 1
				self.list.append((inf, formItem))

			elif inf['type'] == "text" or inf['type'] == "textarea":
				formItem = wx.StaticText(self.sw, -1, inf['label'])
				if inf.has_key("tip"):
					formItem.SetToolTip(wx.ToolTip(inf['tip']))
				self.sizer.Add(formItem, (row, 0), wx.DefaultSpan, wx.ALIGN_LEFT)
				if inf["type"] == "text":
					if inf.has_key("value") and inf['value'] != "":
						formItem = wx.TextCtrl(self.sw, -1, inf['value'][0])
					else:
						formItem = wx.TextCtrl(self.sw, -1, "")
				else: # type == "textarea"
					if inf.has_key("value") and inf['value'] != "":
						formItem = wx.TextCtrl(self.sw, -1, inf['value'][0], style=wxTE_MULTILINE)
					else:
						formItem = wx.TextCtrl(self.sw, -1, "", style=wx.TE_MULTILINE)
				if inf.has_key("tip"):
					formItem.SetToolTip(wx.ToolTip(inf['tip']))
				self.sizer.Add(formItem, (row, 1), wx.DefaultSpan, wx.EXPAND)
				row += 1
				self.list.append((inf, formItem))

			elif inf['type'] == "select":
				formItem = wx.StaticText(self.sw, -1, inf['label'])
				self.sizer.Add(formItem, (row, 0), wx.DefaultSpan, wx.ALIGN_LEFT)
				formItem = wx.Choice(self.sw, -1, (-1, -1), (-1, -1), inf['radiolabels'], name=inf['name'])
				formItem.SetSelection(0)
				self.sizer.Add(formItem, (row, 1), wx.DefaultSpan, wx.EXPAND)
				row += 1
				self.list.append((inf, formItem))

			elif inf['type'] == "radio":
				formItem = wx.StaticText(self.sw, -1, inf['label'])
				if inf.has_key("tip"):
					formItem.SetToolTip(wx.ToolTip(inf['tip']))
				self.sizer.Add(formItem, (row, 0), wx.DefaultSpan, wx.ALIGN_LEFT)
				row += 1
				for rbt in range(len(inf['radiolabels'])):
					# create the new radio button
					formItem = wx.RadioButton(self.sw, label=inf['radiolabels'][rbt], style=0)
					formItem.id = rbt
					if inf.has_key("radiotips"):
						formItem.SetToolTip(wx.ToolTip(inf['radiotips'][rbt]))
					self.sizer.Add(formItem, (row, 1), (1,1), wx.ALIGN_LEFT)
					row += 1
					self.list.append((inf, formItem))
				if inf['name'] == "upload_license":
					self.licenses = (inf['value'], inf['radiolabels'])

			elif inf['type'] == "about":
				if inf['name'] == "cc_remix_search_result" or inf['name'] == "cc_remix_source_choice" :
					formItem = wx.StaticText(self.sw, -1, inf['label'])
					self.sizer.Add(formItem, (row, 0), (1,2), wx.EXPAND)
					row += 1
				elif inf['name'] == "cc_remix_license_notice":
					formItem = wx.StaticText(self.sw, -1, inf['label'])
					self.sizer.Add(formItem, (row, 0), (1,2), wx.EXPAND)
					row += 1
					self.isRemix = True
		
		# get items values from previous forms
		if self.isSubmit():
			self.getPrevValues()

		self.sw.Fit()
		# register for future storage events after validating our
	        # storage-specific settings
	        self.storage.registerEvents()	
		

	def onChanged(self, event):
	        if event.direction:
        		self.init()

	def onChanging(self, event):
		if event.direction:
			if not(self.isSubmit()):
				# if it's not the submission form
			        # show an alert
			        wx.MessageDialog(None, _("You need to fill the submission form first!"), _("Error"), wx.OK).ShowModal()
				# veto the event -- don't allow the page to change w/o correction
				event.Veto()

	def isSubmit(self):
		"""Verify if it's a final submission page"""
		submit = False
		for inf in self.values:
			if inf[0] == "form_submit":
				self.verifyValues()
				self.storage.values = self.values
				self.storage.file_name = self.file_name
				submit = True
		return submit
			

	def search(self, event):
		if self.accept_remixes:
		        self.values.append(("accept_remixes", "Accept"))
		self.values.append(("search", "Search"))
		self.verifyValues()
		self.init(self.values)
		
	def accept(self, event):
	        self.values.append(("accept_remixes", "Accept"))
		self.verifyValues()
		self.init(self.values)

	def verifyValues(self):
		for i in self.list:
			if i[0]['type'] == "select":
				self.values.append((i[0]['name'], i[0]['value'][i[1].GetSelection()]))
			elif i[0]['type'] == "text" or i[0]['type'] == "textarea":
				self.values.append((i[0]['name'], str(i[1].GetValue())))
				if i[0]['name'] == "upload_name":
					self.file_name = str(i[1].GetValue())
			elif i[0]['type'] == "checkbox":
				if i[1].IsChecked():
					self.values.append((i[0]['name'], "checked"))
			elif i[0]['type'] == "radio":
				if i[1].GetValue():
					self.values.append((i[0]['name'], i[0]['value'][i[1].id]))
	def getPrevValues(self):
		"""Get values provided by user in previous windows"""
		# get license if it's not a remix
		if not(self.isRemix):		
			license = p6.api.findField('license', p6.api.getApp().items[0])
			license_xml = etree.fromstring(p6.api.getApp().license_doc)
			license_name = license_xml.find('license-name').text
			license_label = ""

			# adapted nomenclature
			lv = -1
			for lic_value in self.licenses[0]:
				lv += 1
				lic_converter = {
				"attribution": "by",
				"noncommercial": "by-nc",
				"share-alike": "by-sa",
				"noderives": "by-nd"
				}
				if lic_converter.has_key(lic_value):
					lic_value = lic_converter[lic_value]
				# verify if license is allowed by server
				if re.search(lic_value, license, 0) != None:
					license_label = self.licenses[1][lv]
			# if it's not possible to submit files under this license, report to the user
			if license_label == "": 
				wx.MessageDialog(None, _("It's not possible to submit files to %s under %s license! Choose another one in this form." % (self.storage.title, license_name)), _("Warning"), wx.OK).ShowModal()

		# get work's name, tags, description
		for field in self.list:
			if field[0]['name'] == "upload_name":
				field[1].SetValue(p6.api.findField('title', p6.api.getApp().items[0]))
			elif field[0]['name'] == "upload_tags":
				field[1].SetValue(p6.api.findField('keywords', p6.api.getApp().items[0]))
			elif field[0]['name'] == "upload_description":
				field[1].SetValue(str(p6.api.findField('description', p6.api.getApp().items[0])) + "\n" + str(p6.api.findField('holder', p6.api.getApp().items[0])) + "   " + str(p6.api.findField('year', p6.api.getApp().items[0])))
			elif field[0]['name'] == "upload_license" and field[1].GetLabel() == license_label:
				field[1].SetValue(True)
			
	XRCID = "SUBMISSION_FORM"
	PAGE_XRC = """
<resource>
  <object class="wxPanel" name="%s">
    <object class="wxFlexGridSizer">
      <cols>1</cols>
      <rows>1</rows>
      <growablecols>0</growablecols>
      <growablerows>0</growablerows>
    </object>
  </object>
</resource>
	""" % XRCID

class CCHostFinalPage(ccwx.xrcwiz.XrcWizPage):
	"""Display results"""
	zope.interface.implements(p6.ui.interfaces.IWizardPage)

	def __init__(self, parent, storage, headline=_('Upload Complete')):
		"""
	        @param parent: Parent window
	        @type parent: L{wx.Window}
	
	        @param headline: Title to display above the wizard page
	        @type headline: String
	        """

	        ccwx.xrcwiz.XrcWizPage.__init__(self, parent,
                	                        self.PAGE_XRC, self.XRCID, headline)

		self.SetSizer(wx.GridBagSizer(vgap=3, hgap=3))
		self.GetSizer().AddGrowableCol(0)

        	self.storage = storage

	def init(self):
		self.GetSizer().Clear(True)
		self.Fit()
		row = 0
		for result in self.storage.uploads:
			if result[0]: # upload succeeded
				self.GetSizer().Add(wx.StaticText(self, -1, "Your work has been uploaded to %s!" % self.storage.title), (row,0), wx.DefaultSpan, wx.EXPAND)
				row += 1
			else: # upload failed
				self.GetSizer().Add(wx.StaticText(self, -1, "Your work has NOT been uploaded to %s" % self.storage.title), (row,0), wx.DefaultSpan, wx.EXPAND)
				row += 1
			if result[1] != None:
				self.GetSizer().Add(wx.StaticText(self, -1, "Your can view your work online at:\n"), (row,0), wx.DefaultSpan, wx.EXPAND)
				row += 1
				self.GetSizer().Add(wx.lib.hyperlink.HyperLinkCtrl(self, -1, result[1]), (row, 0), wx.DefaultSpan, wx.ALIGN_CENTER_HORIZONTAL)
				row += 1
			if result[2] != "":
				self.GetSizer().Add(wx.StaticText(self, -1, "The error reason:\n %s" % result[2]), (row,0), wx.DefaultSpan, wx.ALIGN_LEFT)
				row += 1
		self.Fit()

	def onChanged(self, event):
		self.init()

	XRCID = "CCHOST_UPLOAD"
	PAGE_XRC = """
<resource>
  <object class="wxPanel" name="%s">
  </object>
</resource>
	""" % XRCID

