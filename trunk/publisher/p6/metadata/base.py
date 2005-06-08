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
