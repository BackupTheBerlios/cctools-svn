import zope.interface

class IMetadataGroup(zope.interface.Interface):
    id = zope.interface.Attribute("")
    title = zope.interface.Attribute("")
    description = zope.interface.Attribute("")

    fields = zope.interface.Attribute("")
    appliesTo = zope.interface.Attribute("")
    
    def __call__():
        """Returns the values of all fields as a dictionary."""

    def getFields():
        """Return a list of the field objects this group contains."""

class IMetadataField(zope.interface.Interface):
    id = zope.interface.Attribute("")
    key = zope.interface.Attribute("A fully qualified key for this field.")
    label = zope.interface.Attribute("")
    type = zope.interface.Attribute("")
    appliesTo = zope.interface.Attribute("")

class IMetadataStorage(zope.interface.Interface):
    # metadata interface

    def setMetaValue(key, value):
        """Set the value of a metadata key; if the key is not previously
        defined, create it."""

    def getMetaValue(key):
        """Returns a metadata value.  If the key does not exist, raises a
        KeyError Exception."""

    def keys():
        """Returns a sequence of valid metadata keys."""

    def metadata():
        """Returns a dictionary-like object containing the key-value pairs
        of metadata defined for this item."""

class IXmlString(zope.interface.Interface):
    xml = zope.interface.Attribute("")
    
