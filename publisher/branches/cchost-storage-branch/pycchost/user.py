"""User-related support functions for CCHost Installation access."""

import sys
import urllib
import HTMLParser


def validate(username, password, cchost_url, Request, urlopen):
    """Confirm that the username/password combination is valid for cchost_url ccHost Installation;
    return True if valid, otherwise return False."""

    loginurl =  cchost_url + "?ccm=/media/login"
    values = {'user_name' : username, 'user_password' : password, 'userlogin' : 'classname'}
    txdata = urllib.urlencode(values)
    txheaders =  {'User-agent' : 'ccPublisher'}
    try:
        req = Request(loginurl, txdata, txheaders) # create a request object
        handle = urlopen(req)
    except IOError, e:
	raise
    else:
        return is_logged_in(handle)

        
def is_logged_in(handle):
    """Start and feed HTMLParser"""
    htmlSource = handle.read()
    p = userParser()
    p.feed(htmlSource)
    p.close()
    return p.logged_in
    

class userParser(HTMLParser.HTMLParser):
    """Parse login page to verify if user is logged in"""
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.logged_in = True
    def handle_starttag(self, tag, attrs):
        if tag=='form':
            for atribute in attrs:
                if atribute[0] == "id" and atribute[1] == "userloginform":
                    self.logged_in = False

