"""User-related support functions for CCHost Installation access."""

import sys

def loader():
    """Try to import cookielib or ClientCookie"""

    cj = None
    ClientCookie = None
    cookielib = None
    
    try:  # see if cookielib is available
        import cookielib            
    except ImportError:
        pass
    else:
        import urllib2    
        urlopen = urllib2.urlopen
        cj = cookielib.LWPCookieJar()  
        Request = urllib2.Request
    
    if not cookielib:  # if importing cookielib fails, try ClientCookie
        try:                                            
            import ClientCookie 
        except ImportError:
            raise
        else:
            urlopen = ClientCookie.urlopen
            cj = ClientCookie.LWPCookieJar()
            Request = ClientCookie.Request

    # install CookieJar so that it is used as the default CookieProcessor in the default opener handler
    if cj != None:
        if cookielib:
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            urllib2.install_opener(opener)
        else:
            opener = ClientCookie.build_opener(ClientCookie.HTTPCookieProcessor(cj))
            ClientCookie.install_opener(opener)
    return Request, urlopen

