import zope.interface

class IMetadataDict(zope.interface.Interface):
    """A dictionary-like interface to metadata.  Does not understand
    "appliesTo", but instead provides a simple interface for the metadata of
    a specific, singular item."""

    def keys():
        """Returns a sequence of key values."""

    def get(key):
        """Returns a specific value for the given key.  Throws an exception
        if key is not a valid key."""

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
    
    def __call__():
        """Returns the current value of the field."""

    def setValue(newValue, item):
        """Set the value for the field to a new value; the optional item
        parameter specifies that this value is only valid for a particular
        item.  The exact semantic is implementation specific."""

class IXmlString(zope.interface.Interface):
    xml = zope.interface.Attribute("")
    
