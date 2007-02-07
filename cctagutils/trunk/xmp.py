import os
import ccrdf
import base

from rdflib.URIRef import URIRef

class XmpMetadata(base.BaseMetadata):

    START_STRINGS = ("<rdf:RDF", )
    END_STRINGS = ("</rdf:RDF>", )
    
    def __init__(self, filename):
        self.filename = filename

        self.__xmp = None

    @property
    def xmp(self):
        """If the XMP data has not been previously extracted or if reload is
        True, scan the file for embedded XMP.  If the data has been previously
        extracted, just return our cached copy.

        Returns XXX.
        """

        if self.__xmp is None:
            # scan the file for XMP

            file_contents = file(self.filename,'r').read()

            for start_tag, end_tag in \
                    zip(self.START_STRINGS, self.END_STRINGS):

                if file_contents.find(start_tag) == -1:
                    continue

                # found the embedded RDF
                rdf_string = file_contents[file_contents.find(start_tag):
                                           file_contents.find(end_tag) + len(end_tag)]

                # store the raw string
                self.xmp_data = rdf_string

                # parse the RDF
                self.__xmp = ccrdf.ccRdf()
                self.__xmp.parse(rdf_string)
                    
        return self.__xmp

    @property
    def work_rdfdict(self):
        """Return the rdfDict for this work."""

        return ccrdf.rdfdict.rdfDict(self.__subject(),
                                     rdfStore = self.xmp.store)
    
    def __subject(self):
        """Return the subject (or likely suspect) for this work."""

        # get a set of the unique subjects, ignoring "fake" ones
        subjects = set([s for s in self.xmp.store.subjects()
                    if str(s)[:2] != "_:"])

        if len(subjects) == 1:
            # only one candidate, must be it
            return subjects.pop()

        # XXX absolutely no f'in idea
        raise KeyError("Unable to determine subject.")

    def __getObjectStr(self, predicate):
        """Return the object specified by self.__subject() and predicate as
        a String; if no such mapping exists, return an empty String."""

        if URIRef(predicate) in self.work_rdfdict:
            return self.work_rdfdict[URIRef(predicate)]
        else:
            return ""
        
    def getTitle(self):
        
        return self.__getObjectStr('http://purl.org/dc/elements/1.1/title')
    
    def getArtist(self):

        return self.__getObjectStr('http://purl.org/dc/elements/1.1/creator')
    
    def getYear(self):

        return self.__getObjectStr('http://ns.adobe.com/xap/1.0/CreateDate')
    
    def getClaim(self):

        return self.__getObjectStr(
            'http://ns.adobe.com/xap/1.0/rights/Copyright')

    def setClaim(self, claim):
        raise NotImplementedError()
    
    def embed(self, license, verification, year, holder):
        """Embed a license claim in the file."""
        raise NotImplementedError()

    def isWritable(self):
        """Returns true if the user has permission to change the metadata."""
        return os.access(self.filename, os.W_OK)

    def properties(self):
        """Return a sequence of property keys for metadata on this object."""

        return [p for p in self.work_rdfdict.store.predicates()]

    def __getitem__(self, key):
        """Return an additional metadata property for this object."""

        return self.__getObjectStr(key)
        
