"""ccPublisher-specific user interface components."""

import os
import socket

import wx
import wx.html
import wx.lib.hyperlink
from wx.xrc import XRCCTRL

import zope.component

import pyarchive.identifier
import pyarchive.exceptions

import p6
import p6.api
import p6.ui.pages.fieldrender
import p6.ui.wizard
from p6.i18n import _

class IdentifierPage(p6.ui.wizard.XRCWizardPage):
    """Identifier selection page class."""

    def __init__(self, parent, storage):
        p6.ui.wizard.XRCWizardPage.__init__(self, parent,
                                        _('Item Identifier'),
                                        os.path.join(p6.api.getResourceDir(),
                                                     "ccpublisher.xrc"),
                                        'IA_IDENTIFIER')

        self.storage = storage
        self.changed = False

        # connect events
        self.Bind(wx.EVT_TEXT, self.updateUrl, XRCCTRL(self, "TXT_IDENTIFIER"))

    def onChanged(self, event):
        """Show the default identifier."""

        try: 
            wx.Yield()
        except wx._core.PyAssertionError, e:
            # ignore assertion errors thrown
            # when yield is called while yielding
            pass
        
        if not(self.changed):
            XRCCTRL(self, "TXT_IDENTIFIER").SetValue(
                self.storage.defaultIdentifier())

    def onChanging(self, event):
        """Validate the proposed identifier."""

        if not(event.direction):
            # user clicked Prev instead of Next
            return
        
        archive_id = XRCCTRL(self, "TXT_IDENTIFIER").GetValue()

        if not(pyarchive.identifier.conforms(archive_id)):
            p6.api.showError(
                _("That identifier does not conform to the "
                "Internet Archive's naming standards.") )
            event.Veto()

        try:
            if not(pyarchive.identifier.available(archive_id)):
                p6.api.showError(
                    _("That identifier is not available.") )
                event.Veto()
        except pyarchive.exceptions.MissingParameterException, e:
            
            p6.api.showError(
                _("That identifier does not conform to the "
                "Internet Archive's naming standards.") )
            event.Veto()
            
        # both tests pass -- store the identifier
        self.storage.identifier = archive_id
        
    def updateUrl(self, event):
        self.changed = True
        
        XRCCTRL(self, "LBL_STATUS").SetLabel(
            pyarchive.identifier.verify_url(
            XRCCTRL(self, "TXT_IDENTIFIER").GetValue()
            )
            )
    

class ArchiveLoginPage(p6.ui.pages.fieldrender.SimpleFieldPage):

    def __init__(self, parent, storage):
        # check if we have persisted values for username/passwd
        persist = zope.component.getUtility(
            p6.metadata.persistance.IMetadataPersistance)
        
        username = persist.query("ia", "username", "")
        password = persist.query("ia", "password", "")
        persist  = persist.query("ia", "persist", False)

        # create the simple page
        fields = [
            p6.metadata.base.metadatafield(p6.metadata.types.ITextField)(
            'username', _('Username'), default=username),
            p6.metadata.base.metadatafield(p6.metadata.types.IPasswordField)(
            'password', _('Password'), default=password),
            p6.metadata.base.metadatafield(p6.metadata.types.IBooleanField)(
            'persist', _('Save your username and password?'), default=persist)
            ]

        description=_("Enter your Internet Archive username and password.  "
                      "If you do not have a username and password, visit "
                      "http://archive.org to create an account.")

        p6.ui.pages.fieldrender.SimpleFieldPage.__init__(self,
                                                         parent,
                                                         'ARCHIVE_LOGIN',
                                                   _('Internet Archive login'),
                                                         fields,
                                                         self.callback,
                                                         description)
        self.storage = storage
        
    def callback(self, value_dict):

        # make sure both a username and password were provided
        if not('username' in value_dict and 'password' in value_dict):
            raise p6.extension.exceptions.ExtensionSettingsException(
                "You must supply both a username and password.")

        # validate the credentials with IA
        try:
            if not(pyarchive.user.validate(value_dict['username'],
                                           value_dict['password'])):

                raise p6.extension.exceptions.ExtensionSettingsException(
                    _("Invalid username or password."))
        except (socket.error, pyarchive.exceptions.CommunicationsError), e:
            raise p6.extension.exceptions.ExtensionSettingsException(
                _("Unable to connect to the Internet Archive to verify username and password."))

        # store the credentials for future use
        # XXX hack!
        self.storage.credentials = (value_dict['username'],
                                    value_dict['password'])

        # check if the user wanted to persist them
        persist = zope.component.getUtility(
            p6.metadata.persistance.IMetadataPersistance)
        
        if value_dict['persist']:
            # store them
            persist.put("ia", "username", value_dict['username'])
            persist.put("ia", "password", value_dict['password'])
            persist.put("ia", "persist", True)
        else:
            # clear the potentially persisted values
            persist.clear("ia", "username")
            persist.clear("ia", "password")
            persist.clear("ia", "persist")


        # register for future storage events after validating our
        # storage-specific settings

        self.storage.registerEvents()

                       
class FinalPage(p6.ui.wizard.XRCWizardPage):
    """Welcome page class."""

    HTTP_LINK_VALUE = None
    
    def __init__(self, parent, storage):
        p6.ui.wizard.XRCWizardPage.__init__(self, parent,
                                        os.path.join(p6.api.getResourceDir(),
                                                     "ccpublisher.xrc"),
                                        'IA_COMPLETE', 'Upload Complete')

        self.storage = storage
        
        # When we change the place holder label to a link label,
        # we store a reference here for handling future updates
        self.__http_link = None

        # Check if we have a link to use
        if self.HTTP_LINK_VALUE is not None:
            self.setItemUrl(self.HTTP_LINK_VALUE)

    def onChanged(self, event):
        """Update the display with the link to the item online."""

        self.setItemUrl(self.storage.uri)

        
    def setItemUrl(self, url):
        """Update the display with a link to the item online."""

        if self.__http_link is None:
            # substitute the link label for the place holder

            # create the new link
            self.__http_link = wx.lib.hyperlink.HyperLinkCtrl(self, -1, url)
            
            # insert it into the sizer
            self.GetSizer().Add(self.__http_link)
            
        else:
            self.__http_link.SetLabel(url)
            self.__http_link.SetURL(url)

        # force the window to redraw
        self.Fit()
