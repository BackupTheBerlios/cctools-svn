#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import HTMLParser
import re

def getForm(url, Request, urlopen):
    """Make a list of dictionaries with all requested information about submission, parsing submission page
    All requested information about submission will be put into a list
    It's a list of dictionaries
    Each dictionary represent one form input.
    dic['type'] -> type of input
    dic['name'] -> identifier of input
    dic['value'] -> list of possible values to input. It's fundamental to hidden type input and radio type too.
    """
    txdata = None
    txheaders =  {'User-agent' : 'ccPublisher', 'Refer' : url}
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
        htmlSource = handle.read()
        p = formParser()
        p.feed(htmlSource)
        p.close()
        return p.form


class formParser(HTMLParser.HTMLParser):
    """Parse submission form page looking for all inputs"""
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.validform = False
        self.inf = {}
        self.form = []
        self.submissiontype = []
    def handle_starttag(self, tag, attrs):
        if tag=='input' and self.validform:
            inf = {}
            inf['value'] = []
            inf['type'] = None
            for atribute in attrs:
                if atribute[0] == "type" or atribute[0] == "name":
                    inf[atribute[0]] = atribute[1]
                elif (atribute[0] == "checked" and atribute[1] == "checked") or atribute[0] == "value":
                    inf['value'].append(atribute[1])
            self.inf = inf
        elif tag=='form':
            for atribute in attrs:
                if atribute[0] == "enctype" and atribute[1] == "multipart/form-data":
                    self.validform = True
    def handle_endtag(self, tag):
        if tag=='input' and self.validform:
            if self.inf['type'] == "submit":
                return
            elif self.inf['type'] == "radio":
                pos = 0
                for elem in self.form:
                    if self.inf['name'] == elem['name']:
                        self.form[pos]['value'].append(self.inf['value'][0])
                        return
                    pos += 1
            self.form.append(self.inf)
        elif tag=='form':
            self.validform = False

