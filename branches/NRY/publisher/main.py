import sys
import os

import wx

import ccwx.xrcwiz

import p6
import p6.metadata
import p6.metadata.base as md
import p6.storage
import p6.ui.wizard

import ccp_pages

class P6(p6.ui.wizard.WizFrame):
    def __init__(self, app):
        p6.ui.wizard.WizFrame.__init__(self, 'FRM_MAIN', app)

        p6.getApp().groups = ccp_pages.metafields()
        self.storage = p6.storage.basic.BasicStorage()
        
        self.setPages(ccp_pages.all_pages(self))

class CcPublisher(p6.ui.wizard.WizApp):
    pass

def main(argv=[]):
   
   # create the application and execute it
   #import wxsupportwiz
   #wxsupportwiz.wxAddExceptHook('http://api.creativecommons.org/traceback.py',
   #                             cctagutils.const.version())

   app = CcPublisher(appname = 'ccPublisher',
                     filename= 'err.log',
                     xrcfile = os.path.join('resources', 'wizard.xrc'),
                     frameclass = P6,
                     )

   app.MainLoop()
   
if __name__ == '__main__':           
    main(sys.argv)

