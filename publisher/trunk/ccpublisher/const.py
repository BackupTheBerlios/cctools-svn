APPNAME = 'ccpublisher'
REPORTING_URL = 'http://roundup.creativecommons.org/autoPost_cgi.py'
REPORTING_APP = 'ccpublisher'

import os
import p6.api

def version():
	
    v = file(os.path.join(p6.api.getResourceDir(), 'version.txt'))\
	.read().strip()
    
    return v
	
