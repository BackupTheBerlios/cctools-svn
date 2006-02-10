APPNAME = 'ccpublisher'

import os
import p6.api

def version():
	
    v = file(os.path.join(p6.api.getAppSupportDir(), 'version.txt'))\
	.read().strip()
    
    return v
	
