
class BaseMetadata:
    def __init__(self, filename):
        self.filename = filename

    def getTitle(self):
        raise NotImplementedError()

    def getArtist(self):
        raise NotImplementedError()

    def getYear(self):
        raise NotImplementedError()

    def getClaim(self):
        raise NotImplementedError()

    def setClaim(self, claim):
        raise NotImplementedError()
    
    def embed(self, license, verification, year, holder):
        """Embed a license claim in the audio file."""
        raise NotImplementedError()

    def isWritable(self):
        """Returns true if the user has permission to change the metadata."""
        raise NotImplementedError()

    def properties(self):
        """Return a sequence of property keys for metadata on this object."""

        raise NotImplementedError()

    def __getitem__(self, key):
        """Return an additional metadata property for this object."""

        raise KeyError("Unknown key %s" % key)
        
