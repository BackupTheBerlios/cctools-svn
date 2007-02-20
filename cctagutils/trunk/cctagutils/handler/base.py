
class BaseMetadata(object):
    def __init__(self, filename):
        self.filename = filename

    def getTitle(self):
        raise NotImplementedError()

    def getArtist(self):
        raise NotImplementedError()

    def getYear(self):
        raise NotImplementedError()

    def getMetadataUrl(self):
        """Return the URL where more metadata on this file may be found;
        this is provided by WCOP in ID3 and the webStatement in XMP."""
        
    def getClaim(self):
        raise NotImplementedError()

    def setClaim(self, claim):
        raise NotImplementedError()

    def getLicense(self):
        """Return the license URL."""

        raise NotImplementedError()
    
    def embed(self, license, verification, year, holder):
        """Embed a license claim in the audio file."""
        raise NotImplementedError()

    def isWritable(self):
        """Returns true if the user has permission to change the metadata."""
        raise NotImplementedError()

    def verify(self):
        """Attempt to verify the embedded claim.  Return one of the VERIFY_*
        constants defined in cctagutil."""

        # XXX import here to avoid circular imports; need to change the
        # implementation in cctagutils.lookup to allow up to verify by
        # passing in a metadata instance.
        
        import cctagutils.lookup

        return cctagutils.lookup.verify(self.filename)
    
    def properties(self):
        """Return a sequence of property keys for metadata on this object."""

        return []
    
    def __getitem__(self, key):
        """Return an additional metadata property for this object."""

        raise KeyError("Unknown key %s" % key)
        
