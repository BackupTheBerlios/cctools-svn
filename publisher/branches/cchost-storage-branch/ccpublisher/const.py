APPNAME = 'ccpublisher'
REPORTING_URL = 'http://roundup.creativecommons.org/autoPost_cgi.py'
REPORTING_APP = 'ccpublisher'

import os
import wx

import p6.api

def version():

    if wx.GetApp() is not None:
        # the application has been created... 
        return file(os.path.join(p6.api.getResourceDir(), 'version.txt'))\
            .read().strip()
    else:
        # check if we're in a source distribution
        if os.path.exists(os.path.join('.', 'resources', 'version.txt')):
            return file(os.path.join('.', 'resources', 'version.txt'))\
                   .read().strip()


    raise Exception("Unable to determine version.")
	
