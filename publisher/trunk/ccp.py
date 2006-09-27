#!/usr/bin/env python

# P6 Bootstrap Script
# copyright 2005-2006, Creative Commons, Nathan R. Yergler
#
# licensed to the public under the GNU GPL version 2.
# see resource/LICENSE.txt for details

import sys
import os
import platform

import wx

import ccpublisher.const as const
from ccpublisher.app import CcPublisher, CcMain

import p6.api
import p6.i18n
import libfeedback

def main(argv=[]):

   # parse any command line options
   (options, args) = p6.app.getParser().parse_args(argv)
   
   # determine the resource path
   try:
       root_dir = os.path.join( os.path.abspath(os.path.dirname(__file__)), 
                                'resources' )
       if platform.system().lower() == 'linux' and \
          not(os.path.exists(os.path.join(root_dir, 'app.zcml'))):
          root_dir = '/usr/local/%s/resources' % const.APPNAME
           
   except NameError, e:
       root_dir = os.path.join( os.path.dirname(sys.executable), 'resources' )


   # initialize i18n machinery
   p6.i18n.initialize(root_dir, locale=options.locale)
   p6.i18n.loadCatalog('ccpublisher')
   
   # create the application 
   app = CcPublisher(appname = 'ccPublisher',
                     rsc_dir = root_dir,
                     filename= 'err.log',
                     xrcfile = 'ccpublisher.xrc',
                     frameclass = CcMain,
                     confFile = 'app.zcml',
                     )

   # configure the application
   app.configure()

   # create the main window
   main = CcMain(app)
   
   # Connect the crash-reporting handler
   ##    libfeedback.wxAddExceptHook(const.REPORTING_URL,
   ##                                const.REPORTING_APP,
   ##                                const.version())

   # start the wizard
   main.start()
   
if __name__ == '__main__':           
    main(sys.argv)

