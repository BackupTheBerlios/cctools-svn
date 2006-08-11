"""User-related support functions for CCHost Installation access."""

import sys
import HTMLParser

def validate(url, Request, urlopen):
    """Confirm that the url is a valid CCHost Installation
    return True if valid, otherwise return False."""

    login_url = url + "?ccm=/media/login"
    txdata = None
    txheaders =  {'User-agent' : 'ccPublisher'}
    try:
        req = Request(login_url, txdata, txheaders) # create a request object
        handle = urlopen(req)
    except IOError, e:
	raise
    else:
        # parse the requested page
        htmlSource = handle.read()
        p = linkParser()
        p.feed(htmlSource)
        p.close()
        return p.valid


class linkParser(HTMLParser.HTMLParser):
    """Parse login page to verify if there are a login form"""
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.valid = False
    def handle_starttag(self, tag, attrs):
        if tag=='form':
            for atribute in attrs:
                if atribute[0] == "id" and atribute[1] == "userloginform":
                    self.valid = True


def title(url, Request, urlopen):
    """Get CCHost Installation's Title"""

    txdata = None
    txheaders =  {'User-agent' : 'ccPublisher'}
    try:
        req = Request(url, txdata, txheaders) # create a request object
        handle = urlopen(req)
    except IOError, e:
	raise
    else:
        # parse requested page
        htmlSource = handle.read()
        p = getTitle() # start the HTMLParser
        p.feed(htmlSource) # take it a html that need be parsed
        p.close()
        if p.title != '' and p.title != None:
            return p.title
        else:
            return 'CCHost Installlation Login'
    return 'CCHost Installlation Login'


class getTitle(HTMLParser.HTMLParser):
    """Get the title of the page, finding tag \"title\" """
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.isTitle = False
        self.title = ''
    def handle_starttag(self, tag, attrs):
        if tag=='title':
            self.isTitle = True
    def handle_endtag(self, tag):
        if tag=='title':
            self.isTitle = False
    # title is all the data between the begin and and of "title" tag
    def handle_data(self, data):
        if self.isTitle:
            self.title += data

