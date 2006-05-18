import urllib2
import elementtree.ElementTree as etree

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
        d = etree.fromstring(self.__lc_doc)

        licenses = d.findall('license')

        for l in licenses:
            lc[l.attrib['id']] = l.text
            
        return lc
        
    def fields(self, license, lang='en'):
        """Retrieves details for a particular license."""

        l_url = '%s/license/%s' % (self.root, license)

        # retrieve the license source document
        self.__l_doc = urllib2.urlopen(l_url).read()

        d = etree.fromstring(self.__l_doc)

        self._cur_license = {}
        keys = []
        
        fields = d.findall('field')

        for field in fields:
            f_id = field.attrib['id']
            keys.append(f_id)
            
            self._cur_license[f_id] = {}

            self._cur_license[f_id]['label'] = field.find('label').text
            self._cur_license[f_id]['description'] = \
                              field.find('description').text
            self._cur_license[f_id]['type'] = field.find('type').text
            self._cur_license[f_id]['enum'] = {}

            # extract the enumerations
            enums = field.findall('enum')
            for e in enums:
                e_id = e.attrib['id']
                self._cur_license[f_id]['enum'][e_id] = \
                     e.find('label').text

        self._cur_license['__keys__'] = keys
        return self._cur_license

    def issue(self, license, answers, workinfo={}, lang='en'):
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
          <work-info>
        """ % (answer_xml, license)

        for key in workinfo:
            answer_xml = """%s
            <%s>%s</%s>""" % (answer_xml, key, workinfo[key], key)

        answer_xml = """%s
          </work-info>
        </answers>
        """ % (answer_xml)

        # retrieve the license source document
        try:
            self.__a_doc = urllib2.urlopen(l_url,
                                     data='answers=%s' % answer_xml).read()
        except urllib2.HTTPError:
            self.__a_doc = ''
            
        return self.__a_doc
