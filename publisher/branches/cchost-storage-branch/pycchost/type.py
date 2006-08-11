"""User-related support functions for CCHost Installation access."""

import sys
import HTMLParser
import re

def getSubmissionTypes(url, Request, urlopen):
    """Return a list of all submission types enabled"""

    url =  url + "?ccm=/media/submit"
    txdata = None
    txheaders =  {'User-agent' : 'publishcchost', 'Refer' : url}
    try:
        req = Request(url, txdata, txheaders) # create a request object
        handle = urlopen(req)
    except IOError, e:
        print 'Failed to open "%s".' % url
        if hasattr(e, 'code'):
            print 'Failed with error code - %s.' % e.code
        elif hasattr(e, 'reason'):
            print "The error reason:", e.reason
            print "This usually means the server doesn't exist, is down, or we don't have an internet connection."
        sys.exit(2)
    else:
        # parse submission page
        htmlSource = handle.read()
        p = submissionParser()
        p.feed(htmlSource)
        p.close()
        return p.submissiontype
    return 'CCHost Installlation Login'


class submissionParser(HTMLParser.HTMLParser):
    """Parse submission page looking for all possible submission type page"""
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

