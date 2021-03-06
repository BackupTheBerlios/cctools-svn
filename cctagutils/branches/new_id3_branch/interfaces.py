import zope.interface

class IMetadata(zope.interface.Interface):
    """An interface to an embedded metadata implementation."""

    def openFile(filename):
        """Open a file and construct a metadta instance around it."""
        
    def getTitle():
        """Return embedded title information."""

    def getHolder():
        """Return embedded copyright holder information."""

    def getYear():
        """Return embedded year of copyright."""

    def getClaim():
        """Return embedded license claim."""

    def setClaim(claim):
        """Update embedded license claim with the specified text."""

    def getLicenseUrl():
        """Return the license url this object is licensed under."""

    def setLicenseUrl(license):
        """Set the URL of the license under which this file is released."""

    def getMetadataUrl():
        """Return the url containing the metadata for this object."""

    def setMetadataUrl(metadata_url):
        """Set the URL of an external metadata store; the external metadata
        may include license verification information."""
        
    def isWritable():
        """Returns true if the user has permission to change the metadata."""
