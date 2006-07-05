"""User-related support functions for CCHost Installation access."""

import os.path
import sys
import urllib


def loader():
    """Try to import some cookielib, urllib2, or ClientCookie"""

    cj = None
    ClientCookie = None
    cookielib = None
    
    try:                                    # Let's see if cookielib is available
        import cookielib            
    except ImportError:
        pass
    else:
        import urllib2    
        urlopen = urllib2.urlopen
        cj = cookielib.LWPCookieJar()       # This is a subclass of FileCookieJar that has useful load and save methods
        Request = urllib2.Request
    
    if not cookielib:                   # If importing cookielib fails let's try ClientCookie
        try:                                            
            import ClientCookie 
        except ImportError:
            import urllib2
            urlopen = urllib2.urlopen
            Request = urllib2.Request
        else:
            urlopen = ClientCookie.urlopen
            cj = ClientCookie.LWPCookieJar()
            Request = ClientCookie.Request
            
    ####################################################
    # We've now imported the relevant library - whichever library is being used urlopen is bound to the right function for retrieving URLs
    # Request is bound to the right function for creating Request objects
    # Let's load the cookies, if they exist. 

    if cj != None:  # now we have to install our CookieJar so that it is used as the default CookieProcessor in the default opener handler
        if cookielib:
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            urllib2.install_opener(opener)
        else:
            opener = ClientCookie.build_opener(ClientCookie.HTTPCookieProcessor(cj))
            ClientCookie.install_opener(opener)

    #=======================================================================================
    return Request, urlopen
