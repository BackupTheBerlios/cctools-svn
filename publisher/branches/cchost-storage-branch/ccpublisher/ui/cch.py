"""ccPublisher-specific user interface components."""

import os
import socket

import wx
import wx.html
import wx.lib.hyperlink
from wx.xrc import XRCCTRL

import ccwx
import zope.interface
import pycchost.exceptions

import p6
import p6.api
import p6.ui.pages.fieldrender
from p6.i18n import _

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

        # verify if the url is a valid ccHost Installation
        try:
            if not(pycchost.location.validate(value_dict['url'], self.storage.Request, self.storage.urlopen)):
                raise p6.extension.exceptions.ExtensionSettingsException(
                    _("Invalid URL."))
        except (socket.error, pycchost.exceptions.CommunicationsError), e:
            raise p6.extension.exceptions.ExtensionSettingsException(
                _("Unable to connect to the CCHost to verify username and password."))


        # store the valid url
        theurl = value_dict['url']
        if theurl[len(theurl)-1] != '/':
            theurl = theurl + "/"
        self.storage.location = theurl
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
        except (socket.error, pycchost.exceptions.CommunicationsError), e:
            raise p6.extension.exceptions.ExtensionSettingsException(
                _("Unable to connect to the CCHost to verify username and password."))



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
	storage providers and allows the user to select one or more.
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
		self.GetSizer().Clear()

		#get a list of submission types and their links
		list =  pycchost.type.getSubmissionTypes(self.storage.location, self.storage.Request, self.storage.urlopen)
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

