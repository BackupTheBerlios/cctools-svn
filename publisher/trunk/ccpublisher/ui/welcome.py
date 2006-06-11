"""ccPublisher-specific user interface components (non-storage)"""

import os
import webbrowser

import wx
import wx.html
import wx.lib.hyperlink
from wx.xrc import XRCCTRL

import ccwx
import p6.api
import p6.i18n

from p6.i18n import _

from ccpublisher.const import version

class WelcomePage(ccwx.xrcwiz.XrcWizPage):
    """Welcome page class."""

    def __init__(self, parent):
        ccwx.xrcwiz.XrcWizPage.__init__(self, parent,
                                        os.path.join(p6.api.getResourceDir(),
                                                     "ccpublisher.xrc"),
                                        'CCTAG_WELCOME', _('Welcome'))

        # connect the How Does This Work button
        self.Bind(wx.EVT_BUTTON, self.onHelp, XRCCTRL(self, "HELP_WHAT_TYPES"))
        
    def onHelp(self, event):

        # determine the path name for the locale-specific html file
        html_file_name = os.path.join(p6.api.getResourceDir(), 'locale',
                                      p6.i18n.getLocale(), 'welcome.html')

        # see if it exists
        if not(os.path.exists(html_file_name)):

            # fall back to the English version
            html_file_name = os.path.join(p6.api.getResourceDir(),
                                          'locale', 'welcome.html')

        if os.path.exists(html_file_name):
            # if the file exists, load it and display 
            html_file = file(html_file_name, 'r')

            help = HtmlHelp(self, 'ccPublisher',
                            html_file.read() % (version(),
                                         os.path.join(
                p6.api.getResourceDir(),'publishguy_small.gif')
                                         )
                            )
            help.Show()
        

class WebbrowserHtml(wx.html.HtmlWindow):
    def OnLinkClicked(self, linkinfo):
        webbrowser.open( linkinfo.GetHref(), True, True )


class HtmlHelp(wx.Dialog):
    def __init__(self, parent, title, source):
        wx.Dialog.__init__(self, parent, -1, title,)
        html = WebbrowserHtml(self, -1, size=(420, -1))
        if "gtk2" in wx.PlatformInfo:
            html.SetFonts('','',[wx.html.HTML_FONT_SIZE_1,
                                 wx.html.HTML_FONT_SIZE_2,
                                 10,
                                 wx.html.HTML_FONT_SIZE_4,
                                 wx.html.HTML_FONT_SIZE_5,
                                 wx.html.HTML_FONT_SIZE_6,
                                 wx.html.HTML_FONT_SIZE_7,
                                 ]
                          )
        #    html.NormalizeFontSizes()
        html.SetPage(source)
        btn = html.FindWindowById(wx.ID_OK)
        ir = html.GetInternalRepresentation()
        html.SetSize( (ir.GetWidth()+25, ir.GetHeight()+25) )
        self.SetClientSize(html.GetSize())
        self.CentreOnParent(wx.BOTH)
