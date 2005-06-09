import weakref

import zope.component
import zope.interface

import p6
import p6.api
import persistance
import interfaces
import events

DEFAULT_KEY = '__p6_default__'

def NoOp(value):
    """A no-op validator used by default."""
    return None
    
def metadatafield(fieldType):
    
    class MetadataField:
        zope.interface.implements(interfaces.IMetadataField, fieldType)

        
        def __init__(self, id, label='',
                     choices=[], default='',
                     description='', tip='',
                     validator = None,
                     persist=False):

            # store the default values
            self.id = id
            self.label = label
            self.choices = choices
            self.default = default
            self.type = fieldType
            self.tip = tip
            self.description = description
            self.validator = validator or NoOp
            self.persist = persist

    return MetadataField


class MetadataGroup:
    zope.interface.implements(interfaces.IMetadataGroup)

    def __init__(self, id, appliesTo, title='', description='', fields=[],
                 persistMode='always'):

        self.id = id
        self.title = title or self.id
        self.description = description
        
        self.fields = fields
        self.appliesTo = appliesTo

        self.persistMode = persistMode

        # finalize field initialization
        for field in self.fields:
            # initialize the .group attribute on field
            field.group = weakref.ref(self)

    def getFields(self):
        return self.fields

class BasicMetadataStorage(object):
    zope.interface.implements(interfaces.IMetadataStorage)
    
    # metadata interface
    def __init__(self):
        self.__meta = {}

    def setMetaValue(self, field, value):
        """Set the value of a metadata key; if the key is not previously
        defined, create it."""

        # store the value
        self.__meta[field.id] = value

    def getMetaValue(self, key, default=None):
        """Returns a metadata value.  If the key does not exist, raises a
        KeyError Exception."""

        if default is None:
            return self.__meta[key]
        else:
            try:
                return self.__meta[key]
            except KeyError, e:
                return default

    def keys(self):
        """Returns a sequence of valid metadata keys."""

        return self.__meta.keys()

    def metadata(self):
        """Returns a dictionary-like object containing the key-value pairs
        of metadata defined for this item."""

        return self.__meta

## class BasicMetadataPersistance(object):
##     zope.interface.implements(interfaces.IMetadataPersistance)

##     def __init__(self, filename):
##         self.shelf = shelve.open(filename, writeback=False)

##     def __del__(self):
##         self.shelf.close()
        
##     def storeKey(self, item, group, field):
##         """Store the specified group-> field for future use."""

##         if self.shelf.has_key(item.getIdentifier()):
##             p_dict = self.shelf[group.id]
##         else:
##             p_dict = {}

##         # retrieve the value
##         p_dict.setdefault(group.id, {})[field.id] = \
##                                     interfaces.IMetadataStorage(item).getMetaValue(field.id)

##         # store the metadata back to the shelf
##         self.shelf[item.getIdentifer()] = p_dict

##     def loadKey(self, item, group, field):
##         """Load the specified group-> field from persistant storage.
##         If not found, raises a KeyError. """
        
##         return self.shelf[item.getIdentifier()][group.id][field.id]

##     def loadKey(self, item, group, field, default):
##         """Load the specified group-> field from persistant storage.
##         If not found, returns the value of default."""

##         try:
##             return self.loadKey(item, group, field)
##         except KeyError, e:
##             return default
        

