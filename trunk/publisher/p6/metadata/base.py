"""
Base metadata field and group support.
"""

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
    """A no-op validator used by default when no custom
    validator is specified."""
    return None
    
def metadatafield(fieldType):
    """Returns a MetadataField class object (implementing the
    L{p6.metadata.interfaces.IMetadataField} interface) which is
    also marked as implementing the specified fieldType."""
    
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
    """Basic implementation of L{p6.metadata.interfaces.IMetadataGroup}.
    Used for grouping metadata fields into logical groups.
    """
    
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
        """Returns a list of fields this group contains.

        @rtype: sequence
        """
        return self.fields

class BasicMetadataStorage(object):
    """Reference implementation of L{p6.metadata.interfaces.IMetadataStorage};
    provides facilities for storing and retrieving metadata values.
    """
    
    zope.interface.implements(interfaces.IMetadataStorage)
    
    # metadata interface
    def __init__(self):
        self.__meta = {}

    def setMetaValue(self, field, value):
        """Set the value of a metadata field.

        @param field: The field to set the value for.
        @ptype field: implements L{p6.metadata.interfaces.IMetadataField}

        @param value: The new value for the field.
        """

        # store the value
        self.__meta[field.id] = value

    def getMetaValue(self, key, **kwargs):
        """Returns a metadata value.  If the key does not exist and no default
        is specified, raises a KeyError Exception.

        @param key: The field to retrieve the value of.
        @keyword default: (optional) The value to return if key is not found.

        @raise KeyError: If the field is not found and no default is specified.
        """

        if 'default' not in kwargs:
            return self.__meta[key]
        else:
            try:
                return self.__meta[key]
            except KeyError, e:
                return kwargs['default']

    def keys(self):
        """Returns a sequence of metadata keys which have values.

        @rtype: sequence
        """

        return self.__meta.keys()

    def metadata(self):
        """Returns a dictionary-like object containing the key-value pairs
        of metadata defined for this item.

        @rtype: dict"""

        return self.__meta
