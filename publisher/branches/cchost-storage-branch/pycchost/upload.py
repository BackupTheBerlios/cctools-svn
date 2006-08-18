"""User-related support functions for CCHost Installation access."""

import sys
import mimetypes, mimetools
import HTMLParser
import re
import form

def post_multipart(url, fields, files, urlopen, Request):
    """
    Post fields and files to an http host as multipart/form-data.
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return the server's response page.
    """
    content_type, body = encode_multipart_formdata(fields, files)
    headers = {'Content-Type': content_type,'Content-Length': str(len(body)),
               'User-agent' : 'ccPublisher'}
    try:
        req = Request(url, body, headers) # create a request object
        handle = urlopen(req)
    except IOError, e:
	raise
    return handle.read()

def encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = mimetools.choose_boundary()
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % get_content_type(filename))
        L.append('')
       	try:
	        L.append(value())
        except IOError, e:
                print 'Failed to open file.'
                print e
                sys.exit(2)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


class uploadParser(HTMLParser.HTMLParser):
    """Parse upload response"""
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.uploadSucceeded = False
        self.url = None
	self.isPrompt = False
        self.isError = False
        self.error = ""
    def handle_starttag(self, tag, attrs):
        if tag=='a':
            for atribute in attrs:
                if atribute[0] == "href" and self.isPrompt and self.isFileLink(atribute[1]):
                    self.uploadSucceeded = True
                    self.url = atribute[1]
	elif tag=='div':
	    for atribute in attrs:
		if atribute[0] == "class" and atribute[1] == "cc_system_prompt":
		    self.isPrompt = True
        elif tag=='td':
            for atribute in attrs:
                if atribute[0] == "class" and atribute[1] == "cc_form_error":
                    self.isError = True
    def handle_endtag(self, tag):
	if tag=='div':
	    self.isPrompt = False
        elif tag=='td' and self.isError:
            self.isError = False
            self.error = form.getString(self.error)
    def handle_data(self, data):
        if self.isError:
            self.error += data
    def isFileLink(self, url):
        if re.search("/media/files/", url, 0) == None:
            return False
        else:
            return True
