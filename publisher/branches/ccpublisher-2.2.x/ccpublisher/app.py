import os
import sys

import wx
from wx.xrc import XRCCTRL

import p6.api
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
        self.SetIcon(wx.Icon(os.path.join(self.app.resource_dir, 'ccp8.ico'),
                             wx.BITMAP_TYPE_ICO))

        # load Mr. Publish
        mr_publish = os.path.join(p6.api.getResourceDir(),
                                  'publishguy_small.gif')
        
        XRCCTRL(self, "IMG_PUBLISHGUY").SetBitmap(
            wx.BitmapFromImage(
            wx.Image(mr_publish, wx.BITMAP_TYPE_GIF)
            )
            )
        

    def getIconList(self):
        if not(getattr(self, '__imgList', None)):
            # create the image list
            self.__imgList = wx.ImageList(33,32)

            self.__imgList.Add(
                wx.Bitmap(os.path.join(self.app.resource_dir, 'cc_doc_33.gif'))
                )
            
        return self.__imgList


       

