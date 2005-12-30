#!/usr/bin/env python

import sys
import os

import wx

import ccwx.xrcwiz

import p6
import p6.metadata.base as md
import p6.storage

class P6(p6.ui.wizard.WizFrame):
    def __init__(self, app):
        p6.ui.wizard.WizFrame.__init__(self, 'FRM_MAIN', app)

class CcPublisher(p6.app.wxpy.WizApp):
    pass

def main(argv=[]):
   
   # create the application and execute it
   #import wxsupportwiz
   #wxsupportwiz.wxAddExceptHook('http://api.creativecommons.org/traceback.py',
   #                             cctagutils.const.version())

   # XXX Move these options to ZCML
   try:
       root_dir = os.path.dirname(__file__)
   except NameError, e:
       root_dir = os.path.dirname(sys.executable)
       
   app = CcPublisher(appname = 'ccPublisher',
                     filename= 'err.log',
                     xrcfile = os.path.join( root_dir, 'resources', 'wizard.xrc'),
                     frameclass = P6,
                     confFile = os.path.join( root_dir, 'app.zcml'),
                     )

   app.MainLoop()
   
if __name__ == '__main__':           
    main(sys.argv)

