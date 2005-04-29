import zope.component
import zope.interface

import p6
import p6.storage.interfaces
import interfaces
import events


def metadatafield(fieldType):
    DEFAULT_KEY = '__p6_default__'
    
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


def metadatagroup(appliesTo):
    class MetadataGroup:
        zope.interface.implements(interfaces.IMetadataGroup, appliesTo)

        def __init__(self, id, title='', fields=[]):

            self.id = id
            self.title = title or self.id

            self.fields = fields
            self.appliesTo = appliesTo

            # register an event handler for metadata field collection
            zope.component.provideHandler(
                zope.component.adapter(events.ICollectGroups)(
                    p6.deinstify(self.handleGetGroups))
                )

        def handleGetGroups(self, event):
            if event.itemType == self.appliesTo or event.itemType is None:
                event.addGroup(self)

        def getFields(self):
            return self.fields

    return MetadataGroup
