import os
import sys

import wx
from wx.xrc import XRCCTRL

import p6.app.wxpy
import p6.ui.wizard

class CcPublisher(p6.app.wxpy.WizApp):
    def __init__(self, appname=None, rsc_dir='.', filename=None,
                 xrcfile=None, frameclass=p6.ui.wizard.WizFrame,
                 confFile='app.zcml'):
        
        # call the superclass constructor
        p6.app.wxpy.WizApp.__init__(self, appname, rsc_dir, filename, xrcfile,
                                    frameclass, confFile)


class CcMain(p6.ui.wizard.WizFrame):
    def __init__(self, app):
        p6.ui.wizard.WizFrame.__init__(self, 'FRM_MAIN', app)

        # set the window icon
        
        # attach the image list to the file selector
        self.__imgList = wx.ImageList(33,33)
        self.__imgList.Add(
            wx.Bitmap(os.path.join(self.app.resource_dir, 'cc_33.gif'))
            )

        XRCCTRL(self, "LST_FILES").SetImageList(self.__imgList,
                                                wx.IMAGE_LIST_NORMAL)

       

