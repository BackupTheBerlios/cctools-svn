"""User-related support functions for CCHost Installation access."""

import sys
import urllib
import HTMLParser
import re

def getForm(url, Request, urlopen, data = None):
    """Make a list of dictionaries with all requested information about submission, parsing submission page
    All requested information about submission will be put into a list
    It's a list of dictionaries
    Each dictionary represent one form input.
    dic['type'] -> type of input
    dic['name'] -> identifier of input
    dic['value'] -> list of possible values to input. It's fundamental to hidden type input and radio type too.
    dic['label']
    dic['tip']
    dic['radiolabels'] -> list of all options labels
    dic['radiotips'] -> list of all options tips
    """
    if data != None:
    	txdata = urllib.urlencode(getDic(data))
    else:
    	txdata = data
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
        self.isLabel = False
        self.isTip = False
        self.isRadioLabel = False
        self.isRadioTip = False

    def handle_starttag(self, tag, attrs):
	if tag=='form':
            for atribute in attrs:
                if atribute[0] == "enctype" and atribute[1] == "multipart/form-data":
                    self.validform = True
	elif self.validform:
	        if tag=='input':
        	    inf = {}
	            inf['value'] = []
	            inf['type'] = "text" # input without type will be text
	            for atribute in attrs:
	                if atribute[0] == "type" or atribute[0] == "name":
	                    inf[atribute[0]] = atribute[1]
	                elif (atribute[0] == "checked" and atribute[1] == "checked") or atribute[0] == "value":
	                    inf['value'].append(atribute[1])
	            self.inf.update(inf)
	        elif tag=='textarea':
	            inf = {}
	            for atribute in attrs:
	                if atribute[0] == "name":
	                    inf['name'] = atribute[1]
		    inf['type'] = "textarea"
	            self.inf.update(inf)
	        elif tag=='div':
	            for atribute in attrs:
	                if atribute[0] == "class":
	                    if atribute[1] == "cc_form_about" or atribute[1] == "cc_remix_license_notice":
	                        inf = {}
	                        inf['type'] = "about"
	                        inf['name'] = atribute[1]
	                        inf['label'] = ""
	                        self.isLabel = True
	                        self.inf = inf
        	            elif atribute[1] == "cc_form_tip":
                	        self.isLabel = False
	                        self.inf['tip'] = ""
	                        self.isTip = True
			    elif atribute[1] == "cc_remix_search_result" or atribute[1] == "cc_remix_search_box" or atribute[1] == "cc_remix_source_choice":
				inf = {}
	                        inf['type'] = "about"
	                        inf['name'] = atribute[1]
	                        self.form.append(inf)
	        elif tag=='td':
	            for atribute in attrs:
	                if atribute[0] == "class" and atribute[1] == "cc_form_label":
	                    self.inf = {}
	                    self.inf['label'] = ""
	                    self.isLabel = True
	        elif tag=='label':
	            self.isRadioLabel = True
	            self.isRadioTip = True
	            for atribute in attrs:
	                if atribute[0] == "for":
	                    self.RadioLabel = [atribute[1], ""]
	                    self.RadioTip = [atribute[1], ""]
		elif tag=='select':
			self.inf = {}
			self.inf['value'] = []
			self.inf['radiolabels'] = []
			for atribute in attrs:
	                	if atribute[0] == "name":
	                    		self.inf['name'] = atribute[1]
		  	self.inf['type'] = "select"
		elif tag=='option':
			self.isRadioLabel = True
			self.RadioLabel = ["", ""]
			for atribute in attrs:
				if atribute[0] == "value":
					self.inf['value'].append(atribute[1])
                    
    def handle_endtag(self, tag):
	if tag=='form':
            self.validform = False
	elif self.validform:
	        if (tag=='input' or tag=='textarea'):
	            if self.inf['type'] == "submit":
		    	self.form.append(self.inf)
	                self.inf = {}
	                return
	            elif self.inf['type'] == "radio":
	                pos = 0
	                for elem in self.form:
	                    if elem.has_key("name") and self.inf['name'] == elem['name']:
	                        self.form[pos]['value'].append(self.inf['value'][0])
	                        self.inf = {}
	                        return
	                    pos += 1
	            self.form.append(self.inf)
	            self.inf = {}
	        elif tag=='div':
	            if self.isLabel == True:
	                self.isLabel = False
	                self.inf['label'] = getString(self.inf['label'])
	                self.form.append(self.inf)
	                self.inf = {}
	            elif self.isTip == True:
	                self.isTip = False
	        elif tag=='td':
	            self.isLabel = False
	        elif tag=='label':
	            self.isRadioTip = False
	            pos = 0
	            for elem in self.form:
	                if elem['type'] == "radio":
	                    for option in elem['value']:
	                        if self.RadioTip[0] == option:
	                            if not(self.form[pos].has_key('radiotips')):
	                                self.form[pos]['radiotips'] = []
	                            self.form[pos]['radiotips'].append(self.RadioTip[1])
	                            return
	                pos += 1
	            if self.isRadioLabel == True:
	                self.isRadioLabel = False
	                pos = 0
	                for elem in self.form:
	                    if elem['type'] == "radio":
	                        for option in elem['value']:
	                            if self.RadioTip[0] == option:
	                                if not(self.form[pos].has_key('radiolabels')):
	                                    self.form[pos]['radiolabels'] = []
	                                self.form[pos]['radiolabels'].append(self.RadioLabel[1])
	                                return
			    elif elem['type'] == "checkbox":
                            	if elem.has_key("name") and self.RadioLabel[0] == elem['name']:
				    self.form[pos]['label'] = self.RadioLabel[1]
	                    pos += 1
	        elif tag=='strong' and self.isRadioLabel:
	            self.isRadioLabel = False
	            pos = 0
	            for elem in self.form:
	                if elem['type'] == "radio":
	                    for option in elem['value']:
	                        if self.RadioTip[0] == option:
	                            if not(self.form[pos].has_key('radiolabels')):
	                                self.form[pos]['radiolabels'] = []
	                            self.form[pos]['radiolabels'].append(self.RadioLabel[1])
	                            return
	                pos += 1
		elif tag=='option':
			self.isRadioLabel = False
			self.inf['radiolabels'].append(self.RadioLabel[1])
		elif tag=='select':
			self.form.append(self.inf)
	            	self.inf = {}

    def handle_data(self, data):
        if self.isLabel:
            self.inf['label'] += data
        elif self.isTip:
            self.inf['tip'] += data
        if self.isRadioLabel:
            self.RadioLabel[1] += data
        if self.isRadioTip:
            self.RadioTip[1] += data

def getString(data):
    """Get some data and return string"""
    result = ""
    for words in re.findall('\S+', data): # get off \n \t spaces ...
        if result != "":
            result += " "
        result += words
    result = re.sub('_', ' ', result)  # substitute _ by space
    return result

def getDic(data):
    """Transform a list into a dictionary"""
    dic = {}
    for elem in data:
    	dic[elem[0]] = elem[1]
    return dic
