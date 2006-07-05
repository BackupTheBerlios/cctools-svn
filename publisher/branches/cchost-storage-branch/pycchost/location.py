"""User-related support functions for CCHost Installation access."""

import os.path
import sys
import urllib, HTMLParser

import exceptions
import loader

def validate(url):
    """Confirm that the url is a valid CCHost Installation
    return True if valid, otherwise return False."""
    Request, urlopen = loader.loader() #import cookies library

    if url[len(url)-1] != '/':
        url = url + "/"
    
    login_url = url + "?ccm=/media/login"
    txdata = None
    txheaders =  {'User-agent' : 'ccPublisher', 'Refer' : login_url}
    try:
        req = Request(login_url, txdata, txheaders) # create a request object
        handle = urlopen(req)
    except IOError, e:
#        print 'We failed to open "%s".' % theurl
#        if hasattr(e, 'code'):
#            print 'We failed with error code - %s.' % e.code
#        elif hasattr(e, 'reason'):
#            print "The error object has the following 'reason' attribute :", e.reason
#            print "This usually means the server doesn't exist, is down, or we don't have an internet connection."
#            sys.exit()
        return False
            
    else:
        htmlSource = handle.read()
        p = linkParser()
        p.feed(htmlSource)
        p.close()
        return p.valid


class linkParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.valid = False
    def handle_starttag(self, tag, attrs):
        if tag=='form':
            for atribute in attrs:
                if atribute[0] == "id" and atribute[1] == "userloginform":
                    self.valid = True
