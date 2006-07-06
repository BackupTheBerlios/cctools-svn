"""User-related support functions for CCHost Installation access."""

import os.path
import sys
import urllib, HTMLParser, re

import exceptions
import loader

def getSubmissionTypes(url, Request, urlopen, cj):
    """Return a list of all submission types enabled"""

    url =  url + "?ccm=/media/submit"
    txdata = None
    txheaders =  {'User-agent' : 'ccPublisher', 'Refer' : url}
    try:
        req = Request(url, txdata, txheaders) # create a request object
        handle = urlopen(req)
    except IOError, e:
#        print 'We failed to open "%s".' % theurl
#        if hasattr(e, 'code'):
#            print 'We failed with error code - %s.' % e.code
#        elif hasattr(e, 'reason'):
#            print "The error object has the following 'reason' attribute :", e.reason
#            print "This usually means the server doesn't exist, is down, or we don't have an internet connection."
#            sys.exit()
        pass
            
    else:
        htmlSource = handle.read()
        p = linkParser()
        p.feed(htmlSource)
        p.close()
        return p.submissiontype
    return 'CCHost Installlation Login'

class linkParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.isLink = False
        self.submissiontype = []
    def handle_starttag(self, tag, attrs):
        if tag=='a':
            for atribute in attrs:
                if atribute[0] == "href" and self.isSubmissionLink(atribute[1]):
                    self.isLink = True
                    self.submissiontype.append(atribute[1])
    def handle_endtag(self, tag):
        if tag=='a':
            self.isLink = False
    def handle_data(self, data):
        if self.isLink:
            self.submissiontype.append(data)
    def isSubmissionLink(self, url):
        if re.search("/media/submit/", url, 0) == None:
            return False
        else:
            return True
