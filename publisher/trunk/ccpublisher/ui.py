"""ccPublisher-specific user interface components."""

import os
import webbrowser

import wx
import wx.html
from wx.xrc import XRCCTRL

import ccwx
import p6.api

from ccpublisher.const import version

class WelcomePage(ccwx.xrcwiz.XrcWizPage):
    """Welcome page class."""

    def __init__(self, parent):
        ccwx.xrcwiz.XrcWizPage.__init__(self, parent,
                                        self.PAGE_XRC,
                                        'CCTAG_WELCOME', 'Welcome')

        # connect the How Does This Work button
        self.Bind(wx.EVT_BUTTON, self.onHelp, XRCCTRL(self, "HELP_WHAT_TYPES"))
        
    def onHelp(self, event):
        help = HtmlHelp(self, 'ccPublisher',
                        MORE_INFO % (version(),
                                     os.path.join(
            p6.api.getAppSupportDir(),'publishguy_small.gif')
                                     )
                        )
        help.Show()
        


    PAGE_XRC="""
    <resource>
      <object class="wxPanel" name="CCTAG_WELCOME">
    <object class="wxFlexGridSizer">
      <cols>1</cols>
      <object class="sizeritem">
        <object class="wxStaticText">
          <label>This tool will help you put your audio and video on the 
Web with a Creative Commons license.

It's simple:</label>
        </object>
      </object>
      <vgap>5</vgap>
      <growablecols>0</growablecols>
      <object class="sizeritem">
        <object class="wxStaticText">
          <label>1) Drag and drop your audio or video files
2) Choose your Creative Commons license
3) Optionally send your Creative Commons licensed files to the Internet Archive, a free hosting service
4) Get a URL where you and your friends can download your file

</label>
        </object>
        <flag>wxGROW</flag>
      </object>
      <object class="sizeritem">
        <object class="wxStaticText">
          <label>Click Next to get started.</label>
        </object>
        <flag>wxEXPAND</flag>
      </object>
      <object class="sizeritem">
        <object class="wxButton" name="HELP_WHAT_TYPES">
          <label>How does this work?</label>
          <style>wxNO_BORDER</style>
        </object>
        <flag>wxALIGN_RIGHT|wxALIGN_BOTTOM</flag>
        <cellpos>2,1</cellpos>
        <cellspan>1,1</cellspan>
      </object>
      <object class="spacer">
        <size>2,2</size>
      </object>
      <growablerows>2</growablerows>
      <growablerows>3</growablerows>
    </object>
    </object>
    </resource>
    """

class FinalPage(ccwx.xrcwiz.XrcWizPage):
    """Welcome page class."""

    def __init__(self, parent):
        ccwx.xrcwiz.XrcWizPage.__init__(self, parent,
                                        self.PAGE_XRC,
                                        'IA_COMPLETE', 'Upload Complete')

    PAGE_XRC="""
<resource>
  <object class="wxPanel" name="IA_COMPLETE">
    <object class="wxFlexGridSizer">
      <cols>1</cols>
      <object class="sizeritem">
        <object class="wxStaticText">
          
          <label>Your work has been uploaded to the Internet Archive.</label>
        </object>
      
        <flag>wxEXPAND</flag>
      </object>
      <growablecols>0</growablecols>
      <object class="sizeritem">
        <object class="wxStaticText">
          
          <label>You can view your work online at:</label>
        </object>
      
        <flag>wxEXPAND</flag>
      </object>
      <object class="spacer">
        
        <size>10,10</size>
      </object>
      <object class="sizeritem">
        <object class="wxStaticText" name="TXT_FINALURL">
          
          <label>%s</label>
        </object>
      
        <flag>wxEXPAND</flag>
      </object>
    </object>
  </object>
</resource>
"""

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

MORE_INFO = """
<html>
<title>ccPublisher</title>
<body bgcolor="#e3e3e3">
<table width="100%%" bgcolor="#729cb3" cellspacing="0" border="0">
<tr><td><font size="+1"><strong>ccPublisher</strong></font><br>
        <font size="-1">version %s</font></td>
    <td align="right"><img src="%s"></td></tr>
</table>
<p><strong>What is ccPublisher?</strong></p>
<p>ccPublisher is a tool which will help you put your audio and video on the
Web with a Creative Commons license.  It will also let you upload your files
to the Internet Archive to take advantage of free hosting.</p>
<p><strong>What files can ccPublisher upload?</strong></p>
<p>ccPublisher will embed a license claim in MP3 audio files.  ccPublisher will let
you upload any audio or video file to the Internet Archive.</p>
<p><strong>What about file sharing networks?</strong></p>
<p>MP3 files licensed using ccPublisher (uploaded to the Internet Archive or self-
hosted) will have an embedded license tag added which some file sharing networks
can detect.  Just drop the files in your shared folder after you finish the
ccPublisher wizard.</p>
<p><strong>Do I need an Internet connection?</strong></p>
<p>Yes, ccPublisher uses Creative Commons web services to create license
information for your files.</p>
</body>
</html>

"""
