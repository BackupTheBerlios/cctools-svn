# Copyright (c) 2004-2005, Nathan R. Yergler, Creative Commons
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
ccrdf.py

Wraps Creative Commons licenses in Python objects; allows creation of new
licenses, parsing of RDF licenses and extraction of license components.
"""

__id__ = "$Id$"
__version__ = "$Revision$"
__copyright__ = '(c) 2003-2004, Nathan R. Yergler'
__license__ = 'licensed under the GNU GPL2'

# import some basic support structure
import sys
import xml.sax.xmlreader
import cStringIO

# import RDF handling facilities
from rdflib.TripleStore import TripleStore
from rdflib.BNode import BNode
from rdflib.Literal import Literal
from rdflib.URIRef import URIRef

from aaronrdf import cc, dc
import rdfdict

# check the version of Python we're running on and
# set Boolean constants if necessary
if (sys.version_info < (2,3)):
    True = 1
    False = 0

class ccLicense(rdfdict.rdfDict):
    """
    Models a Creative Commons license definition.
    """

class ccWork(rdfdict.rdfDict):
    """
    Models work (Dublin Core) information (possibly) related to a Creative
    Commons license.
    """
    
    def licenses(self):
        """
        Returns a list of ccLicense objects describing any licenses
        associated with the work.
        """

        return [n for n in self.store.objects(subject=self.subject,
                                              predicate=cc.license)
                ]

    def addLicense(self, license):
        """
        Attaches a given ccLicense to this work.
        """

        self.store.add( (self.subject, cc.license, str(license)) )
    
class ccRdf(rdfdict.rdfStore):
    """
    Provides RDF parsing and output functions for CC license and work
    definitions.
    """
    
    def works(self):
        """
        Returns a list of works described by the RDF.
        """

        works = []

        for work in self.store.subjects(predicate=None, object=cc.Work):
            works.append(ccWork(work, self.store))

        return works
   
    def licenses(self):
        """
        Returns a list of licenses described by the RDF.
        """

        licenses = []

        # return a list of the generically defined licenses
        for license in self.store.subjects(predicate=None,
                                           object=cc.License):
            licenses.append(ccLicense(license, self.store))

        return licenses

    addWork = rdfdict.rdfStore.append
    addLicense = rdfdict.rdfStore.append
    
