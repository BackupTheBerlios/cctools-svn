"""User-related support functions for CCHost Installation access."""

import os.path
import sys
import urllib
from HTMLParser import HTMLParser

import exceptions
import loader

def validate(username, password, cchost_url):
    """Confirm that the username/password combination is valid for cchost_url ccHost Installation;
    return True if valid, otherwise return False."""

    Request, urlopen  = loader.loader() #import cookies library

    theurl =  cchost_url + "?ccm=/media/login"
    values = {'user_name' : username, 'user_password' : password, 'userlogin' : 'classname'}
    txdata = urllib.urlencode(values)
    txheaders =  {'User-agent' : 'ccPublisher', 'Refer' : theurl}
    try:
        req = Request(theurl, txdata, txheaders) # create a request object
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
        return is_logged_in(handle)
        

    # if we get this far we we're able to validate; raise an exception
    raise exceptions.CommunicationsException()

def is_logged_in(handle):
    htmlSource = handle.read()
    p = linkParser()
    p.feed(htmlSource)
    p.close()
    return p.logged_in
    
class linkParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.logged_in = True
    def handle_starttag(self, tag, attrs):
        if tag=='form':
            for atribute in attrs:
                if atribute[0] == "id" and atribute[1] == "userloginform":
                    self.logged_in = False
    

