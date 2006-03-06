#!/usr/bin/env python

# P6 Bootstrap Script
# copyright 2005-2006, Creative Commons, Nathan R. Yergler
#
# licensed to the public under the GNU GPL version 2.
# see resource/LICENSE.txt for details

import sys
import os
import platform

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'basket')))
print sys.path
import pkg_resources
pkg_resources.require("zope.interface")
pkg_resources.require("zope.component")
pkg_resources.require("zope.configuration")
pkg_resources.require("zope.schema")

import ccpublisher.const as const
from ccpublisher.app import CcPublisher, CcMain

import libfeedback

def main(argv=[]):

   # determine the resource path
   try:
       root_dir = os.path.join( os.path.dirname(__file__), 'resources' )
       if platform.system().lower() == 'linux' and \
              not(os.path.exists(os.path.join(root_dir, 'app.zcml'))):
           root_dir = '/usr/local/%s/resources' % const.APPNAME
           
   except NameError, e:
       root_dir = os.path.join( os.path.dirname(sys.executable), 'resources' )

   # create the application and execute it
   app = CcPublisher(appname = 'ccPublisher',
                     rsc_dir = root_dir,
                     filename= 'err.log',
                     xrcfile = 'wizard.xrc',
                     frameclass = CcMain,
                     confFile = 'app.zcml',
                     )

   # Connect the crash-reporting handler
   libfeedback.wxAddExceptHook(const.REPORTING_URL,
                               const.REPORTING_APP,
                               const.version())

   app.MainLoop()
   
if __name__ == '__main__':           
    main(sys.argv)

