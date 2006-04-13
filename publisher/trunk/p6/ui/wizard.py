"""
Customized wizard framework -- top level window classes.
"""

import wx
import wx.xrc

import zope.interface
import zope.configuration.xmlconfig
import ccwx.xrcwiz

import p6
import p6.api
import interfaces


class WizFrame(ccwx.xrcwiz.XrcWiz):
    """Top level wizard window."""
    
    def __init__(self, xrcid, app):
        """
        @param xrcid: The identifier of the XRC object in the application's
           XRC file which defines our chrome.
        @type xrcid: string

        @param app: The application object.
        @type app: L{wx.App}
        """
        
        ccwx.xrcwiz.XrcWiz.__init__(self, app, app.xrcfile, xrcid)

        self.app = app
        self.setPages([n(self) for n in p6.api.getApp().pages])

    def setPages(self, pages):
        """Updates the list of pages this wizard manages and resets the view
        to the first page.

        @param pages: Sequence of pages implementing
           L{p6.ui.interfaces.IWizardPage}.
        @type pages: sequence
        """

        self.setPageCollection(ccwx.xrcwiz.PageCollection(pages))
        self.addCurrent(None)

        self.pages.current().Show()

        self.SetAutoLayout(True)
        self.Show()
        self.Layout()
    
