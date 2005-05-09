import zope.component
import zope.interface

import p6
import p6.api
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
                     validator = None):

            # store the default values
            self.id = id
            self.label = label
            self.choices = choices
            self.default = default
            self.type = fieldType
            self.tip = tip
            self.description = description
            self.validator = validator or NoOp

    return MetadataField


class MetadataGroup:
    zope.interface.implements(interfaces.IMetadataGroup)

    def __init__(self, id, appliesTo, title='', description='', fields=[]):

        self.id = id
        self.title = title or self.id
        self.description = description
        
        self.fields = fields
        self.appliesTo = appliesTo

    def getFields(self):
        return self.fields

class BasicMetadataStorage(object):
    zope.interface.implements(interfaces.IMetadataStorage)
    
    # metadata interface
    def __init__(self):
        self.__meta = {}

    def setMetaValue(self, key, value):
        """Set the value of a metadata key; if the key is not previously
        defined, create it."""
        
        self.__meta[key] = value
        print self
        print self.__meta
        
    def getMetaValue(self, key):
        """Returns a metadata value.  If the key does not exist, raises a
        KeyError Exception."""

        return self.__meta[key]

    def keys(self):
        """Returns a sequence of valid metadata keys."""

        return self.__meta.keys()

    def metadata(self):
        """Returns a dictionary-like object containing the key-value pairs
        of metadata defined for this item."""

        return self.__meta
