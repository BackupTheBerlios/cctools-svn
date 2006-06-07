"""Basic file selector page; published ItemSelected events."""

import os
import weakref

import wx
import wx.xrc
from wx.xrc import XRCCTRL

import zope.interface
import ccwx.xrcwiz

import p6
import p6.api

from p6.i18n import _
from p6.ui.interfaces import ILabelText

class FileDropTarget(wx.FileDropTarget):
    """ This object implements generic drop target functionality for Files """

    def OnDropFiles(self, x, y, filenames):
        """Bridge dropped files to P6 events."""

        for filename in filenames:
            # check if this is a directory
            if os.path.isdir(filename):
                # we don't support adding directories 
                wx.MessageDialog(None,
                   _("Please drag and drop individual files on this window."), 
                   _("appname") + ": " + _("Error"), wx.OK).ShowModal()
                continue
            
            zope.component.handle(
                p6.storage.events.ItemSelected(
                   p6.storage.items.FileItem(filename)
                   )
                )

class FileListControl(wx.ListCtrl):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1,
                             style=wx.LC_REPORT|wx.LC_VIRTUAL)

        self.SetImageList(p6.api.getApp().GetTopWindow().getIconList(),
                          wx.IMAGE_LIST_NORMAL)
        self.SetImageList(p6.api.getApp().GetTopWindow().getIconList(),
                          wx.IMAGE_LIST_SMALL)

        # set up the list of items and the columns
        self.__items = []
        self.InsertColumn(0, _("Filename"), width=-1)
        self.SetItemCount(0)

        # connect UI events
        self.Bind(wx.EVT_SIZE, self.OnResize, self)
        
        # connect event listeners for updating the user interface
        # listen for item addition events
        zope.component.provideHandler(
            zope.component.adapter(p6.storage.events.IItemSelected)(
                p6.api.deinstify(self.selectItem))
            )

        # listen for item removal events
        zope.component.provideHandler(
            zope.component.adapter(p6.storage.events.IItemDeselected)(
                p6.api.deinstify(self.removeItem))
            )

    def GetVirtualItem(self, index):
        """Return the virtual item we derive the list control item
        from for the specified index."""
        
        return self.__items[index]

    def OnGetItemText(self, item, col):
        """Return the item text."""

        return ILabelText(self.__items[item]).text

    def OnGetItemImage(self, item):
        """Return the image to use for this item."""
        
        # XXX Eventually we'll want to use file-type specific icons
        return 0

    def OnGetItemAttr(self, item):
        """Return the row attributes for this item."""
        
        return None

    def OnResize(self, event):
        """Resize the filename column as the window is resized."""
        
        self.SetColumnWidth(0, self.GetClientSizeTuple()[0])
        event.Skip()
        
    def selectItem(self, event):
        """Responds to ItemSelected events and updates the user interface."""

        # add the item to our list
        self.__items.append(event.item)

        # update the item count
        self.SetItemCount(len(self.__items))
        
    def removeItem(self, event):
        """Responds to ItemDeselected events and updates the user interface."""

        # remove the item from the list
        self.__items.remove(event.item)
        
        # update the item count
        self.SetItemCount(len(self.__items))

    
class FileSelectorPage(ccwx.xrcwiz.XrcWizPage):
    """Page which displays a file selector and publishes events when
    items are selected or deselected.
    """
    zope.interface.implements(p6.ui.interfaces.IWizardPage)

    def __init__(self, parent, headline=_('Select Your Files')):
        """
        @param parent: Parent window
        @type parent: L{wx.Window}

        @param headline: Title to display above the wizard page
        @type headline: String
        """
        
        ccwx.xrcwiz.XrcWizPage.__init__(self, parent,
                                        os.path.join(p6.api.getResourceDir(),
                                                     "p6.xrc"),
                                        "FILE_SELECTOR", headline)

        # initialize the user interface
        self.__initUserInterface()

    def __initUserInterface(self):
        # create the list control for showing selected files
        self.__fileList = FileListControl(self)
        self.GetSizer().Add(self.__fileList, flag=wx.EXPAND|wx.ALL)
            
        # enable dropping files on the list box
        self.__fileList.SetDropTarget(FileDropTarget())

        # connect event handlers for browse button, delete button, delete key
        self.Bind(wx.EVT_BUTTON, self.onBrowse, XRCCTRL(self, "CMD_BROWSE"))
        self.Bind(wx.EVT_BUTTON, self.onDelete, XRCCTRL(self, "CMD_DELETE"))
        self.Bind(wx.EVT_KEY_UP, self.onKeyUp,  self)

    def onBrowse(self, event):
        """Event handler for file selection; publishes ItemSelected events
        when the user picks one or more files."""
        
        fileBrowser = wx.FileDialog(self.GetParent(),
                                 style=wx.OPEN|wx.MULTIPLE|wx.FILE_MUST_EXIST)

        if fileBrowser.ShowModal() == wx.ID_OK:

            for filename in fileBrowser.GetPaths():
                # generate an ItemSelected event for each file
                zope.component.handle(
                    p6.storage.events.ItemSelected(
                       p6.storage.items.FileItem(filename)
                       )
                    )

    def onDelete(self, event):
        """Event handler for file removal; publishes ItemDeselected events."""


        # contstruct a list of items to remove
        to_remove = []
        
        selectedItem = self.__fileList.GetFirstSelected()
        while(selectedItem != -1):

            to_remove.append(
                self.__fileList.GetVirtualItem(selectedItem))
            selectedItem = self.__fileList.GetNextSelected(selectedItem)

        # fire an item deselected event for each
        for item in to_remove:
            
            # publish the de-select event
            zope.component.handle(
                p6.storage.events.ItemDeselected(item)
                )
                
    def onKeyUp(self, event):
        if (event.GetKeyCode() == wx.WXK_DELETE):
            self.onDelete(event)
        
    def validate(self, event):
        # make sure the user has selected at least one file...
        if event.direction:
            # only check if moving forward
            if self.__fileList.GetItemCount() > 0:
                return True
            else:
                # haven't selected anything; show an error message
                wx.MessageDialog(self, _("You must select at least one file."),
                                 _("appname") + ": " + _("Error"),
                                 wx.OK).ShowModal()
                return False
        else:
            # always allow moving back
            return True
    
