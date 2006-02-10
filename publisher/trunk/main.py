#!/usr/bin/env python

import sys
import os
import platform

import wx

import ccwx.xrcwiz

import p6
import p6.metadata.base as md
import p6.storage

import ccpublisher.const as const
from ccpublisher.app import CcPublisher, CcMain

def main(argv=[]):
   
   # create the application and execute it
   #import wxsupportwiz
   #wxsupportwiz.wxAddExceptHook('http://api.creativecommons.org/traceback.py',
   #                             cctagutils.const.version())

   try:
       root_dir = os.path.join( os.path.dirname(__file__), 'resources' )
       if platform.system().lower() == 'linux' and \
              not(os.path.exists(os.path.join(root_dir, 'app.zcml'))):
           root_dir = '/usr/local/%s/resources' % const.APPNAME
           
   except NameError, e:
       root_dir = os.path.join( os.path.dirname(sys.executable), 'resources' )
       
   app = CcPublisher(appname = 'ccPublisher',
                     rsc_dir = root_dir,
                     filename= 'err.log',
                     xrcfile = 'wizard.xrc',
                     frameclass = CcMain,
                     confFile = 'app.zcml',
                     )

   app.MainLoop()
   
if __name__ == '__main__':           
    main(sys.argv)

