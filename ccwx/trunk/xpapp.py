# Copyright (c) 2004-2005, Nathan R. Yergler, Creative Commons
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import platform
import os

import wx

from support import attrdict

class XpApp(wx.App):

    def __init__(self, appname, filename=None):
        self.paths = attrdict()
        self.appname = appname
        wx.App.__init__(self, filename=filename)

        self.OnInitXpApp()
        
    def OnInit(self):
        self.SetAppName(self.appname)

        self.paths = attrdict()
        
        wx.InitAllImageHandlers()
        self.InitPaths()
        self.SetPlatformPaths()

        return True
        
    def InitPaths(self):
        pass
        
    def SetPlatformPaths(self):
        # set any platform-specific parameters
        if platform.system().lower() == 'darwin':
            # set the file path to the XRC resource file
            # to handle the app bundle properly
            self.paths.RESOURCE_DIR = os.path.dirname(sys.argv[0])
    
            # store the preferences and error log in ~/Library/Application Support/ccPublisher
            app_lib_dir = os.path.expanduser('~/Library/Application Support/%s' % self.appname)
            if not(os.path.exists(app_lib_dir)):
                   os.makedirs(app_lib_dir)
                   
            self.paths.APP_LIB_DIR = app_lib_dir
            
        elif platform.system().lower() == 'windows':
            self.paths.RESOURCE_DIR = self.paths.APP_LIB_DIR = os.path.dirname(sys.argv[0])

        elif platform.system().lower() == 'linux':
            # check if the resources directory exists;
            # if not check for /usr/share/ccpublisher
            NIX_RSC_DIR = os.path.join('resources')#os.path.join('usr','share','resources',self.appname)
                   
            self.paths.RESOURCE_DIR = NIX_RSC_DIR

            # reset the folder paths for log file and prefs file
            self.paths.APP_LIB_DIR = os.path.join(os.path.expanduser('~'), '.ccpublisher')
            if not(os.path.exists(self.paths.APP_LIB_DIR)):
                os.makedirs(self.paths.APP_LIB_DIR)
    
