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
    validator = zope.interface.Attribute("An optional callable which returns a string containing an error message if the field's value does not validate.")

    def group():
        """Returns a reference to the group which contains this field."""

class IMetadataProvider(zope.interface.Interface):
    """MetadataProviders give read-only access to metadata attributes."""

    def getMetaValue(key):
        """Returns a metadata value.  If the key does not exist, raises a
        KeyError Exception."""

    def keys():
        """Returns a sequence of valid metadata keys."""

    def metadata():
        """Returns a dictionary-like object containing the key-value pairs
        of metadata defined for this item."""

class IMetadataStorage(IMetadataProvider):
    """Implementors of IMetadataStorage give read-write access to
    metadata attributes."""

    def setMetaValue(key, value):
        """Set the value of a metadata key; if the key is not previously
        defined, create it."""

## class IMetadataPersistance(zope.interface.Interface):
##     """Implements metadata persistance for the framework."""

##     def storeKey(item, group, field):
##         """Store the specified group-> field for future use."""

##     def loadKey(item, group, field):
##         """Load the specified group-> field from persistant storage.
##         If not found, raises a KeyError. """

##     def loadKey(item, group, field, default):
##         """Load the specified group-> field from persistant storage.
##         If not found, returns the value of default."""

