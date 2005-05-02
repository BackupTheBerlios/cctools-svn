import zope.component
import zope.interface

import p6
import p6.api
import interfaces
import events

DEFAULT_KEY = '__p6_default__'

def metadatafield(fieldType):
    
    class MetadataField:
        zope.interface.implements(interfaces.IMetadataField, fieldType)

        
        def __init__(self, id, label='', choices=[], default=''):

            # store the default values
            self.id = id
            self.label = label
            self.choices = choices
            self.default = default
            self.type = fieldType

            # value is stored as a dict to support per-item metadata;
            # in the event the value is set without specifying an item
            # the DEFAULT_KEY is used.
            self.value = {}
            
        def __call__(self):
            if len(self.value) == 1 and DEFAULT_KEY in self.value:
                return self.value[DEFAULT_KEY]
            else:
                return self.value
        
        def setValue(self, newValue, item=DEFAULT_KEY):
            self.value[item] = newValue

    return MetadataField


class MetadataGroup:
    zope.interface.implements(interfaces.IMetadataGroup)

    def __init__(self, id, appliesTo, title='', description='', fields=[]):

        self.id = id
        self.title = title or self.id
        self.description = description
        
        self.fields = fields
        self.appliesTo = appliesTo

        # register an event handler for metadata field collection
        zope.component.provideHandler(
            zope.component.adapter(events.ICollectGroups)(
                p6.api.deinstify(self.handleGetGroups))
            )

    def handleGetGroups(self, event):
        if event.itemType == self.appliesTo or event.itemType is None:
            event.addGroup(self)

    def getFields(self):
        return self.fields
