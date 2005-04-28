import urllib2
import libxml2
import libxslt

class CcRest:
    """Wrapper class to decompose REST XML responses into Python objects."""
    
    def __init__(self, root):
        self.root = root

        self.__lc_doc = None

    def license_classes(self, lang='en'):
        """Returns a dictionary whose keys are license IDs, with the
        license label as the value."""

        lc_url = '%s/%s' % (self.root, 'classes')

        # retrieve the licenses document and store it
        self.__lc_doc = urllib2.urlopen(lc_url).read()

        # parse the document and return a dictionary
        lc = {}
        d = libxml2.parseMemory(self.__lc_doc, len(self.__lc_doc))
        c = d.xpathNewContext()

        licenses = c.xpathEval('//licenses/license')

        for l in licenses:
            lc[l.xpathEval('@id')[0].content] = l.content
            
        return lc
        
    def fields(self, license, lang='en'):
        """Retrieves details for a particular license."""

        l_url = '%s/license/%s' % (self.root, license)

        # retrieve the license source document
        self.__l_doc = urllib2.urlopen(l_url).read()

        d = libxml2.parseMemory(self.__l_doc, len(self.__l_doc))
        c = d.xpathNewContext()
        
        self._cur_license = {}
        keys = []
        
        fields = c.xpathEval('//field')

        for field in fields:
            f_id = field.xpathEval('@id')[0].content
            keys.append(f_id)
            
            self._cur_license[f_id] = {}

            self._cur_license[f_id]['label'] = field.xpathEval('label')[0].content
            self._cur_license[f_id]['description'] = \
                              field.xpathEval('description')[0].content
            self._cur_license[f_id]['type'] = field.xpathEval('type')[0].content
            self._cur_license[f_id]['enum'] = {}

            # extract the enumerations
            enums = field.xpathEval('enum')
            for e in enums:
                e_id = e.xpathEval('@id')[0].content
                self._cur_license[f_id]['enum'][e_id] = \
                     e.xpathEval('label')[0].content

        self._cur_license['__keys__'] = keys
        return self._cur_license

    def issue(self, license, answers, lang='en'):
        l_url = '%s/license/%s/issue' % (self.root, license)

        # construct the answers.xml document from the answers dictionary
        answer_xml = """
        <answers>
          <license-%s>""" % license

        for key in answers:
            answer_xml = """%s
            <%s>%s</%s>""" % (answer_xml, key, answers[key], key)

        answer_xml = """%s
          </license-%s>
        </answers>
        """ % (answer_xml, license)

        
        # retrieve the license source document
        try:
            self.__a_doc = urllib2.urlopen(l_url,
                                     data='answers=%s' % answer_xml).read()
        except urllib2.HTTPError:
            self.__a_doc = ''
            
        return self.__a_doc
