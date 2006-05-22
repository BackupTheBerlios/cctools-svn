"""Storage page for controlling upload process and displaying feedback."""

import wx
from wx.xrc import XRCCTRL

import ccwx.xrcwiz

import zope.component

import p6
import p6.api

class FinalUrlPage(ccwx.xrcwiz.XrcWizPage):
    """Displays a page which validates and stores the item."""
    
    XRCID = "FINAL_URL"

    def __init__(self, parent, headline='Uploading'):
        """
        @param parent: Parent window
        @type parent: L{wx.Window}

        @param headline: Title to display above the wizard page
        @type headline: String
        """
        
        ccwx.xrcwiz.XrcWizPage.__init__(self, parent,
                                        self.PAGE_XRC, self.XRCID, headline)

    PAGE_XRC = """
<resource>
  <object class="wxPanel" name="FINAL_URL">
    <object class="wxFlexGridSizer">
      <cols>1</cols>
      <growablecols>0</growablecols>
      <growablerows>3</growablerows>
      <vgap>10</vgap>
      
      <object class="sizeritem">
        <object name="LBL_MACRO_TASK" class="wxStaticText">
          <label>Done! (XXX)</label>
        </object>
        <flag>wxEXPAND</flag>
      </object>

    </object>
  </object>

</resource>
    """
    
