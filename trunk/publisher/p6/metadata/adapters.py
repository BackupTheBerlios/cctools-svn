import zope.interface
import zope.component

import p6
import interfaces

def groupToXml(metaGroup):
    if metaGroup.appliesTo is not None:
        # != p6.storage.interfaces.IWork:
        elements = "\n".join(["<%s>%s</%s>" % (n.id, n(), n.id) for n in
                   metaGroup.getFields()])
        return "<%s>\n%s\n</%s>" % (metaGroup.id, elements, metaGroup.id)
    else:
        return None


def updateMetadata(event):
    """Reponds to a metadata update event."""

    if event.item is None:
        # This applies to any root item
        for i in p6.api.getApp().items:
            if p6.storage.interfaces.IWork in \
                   zope.interface.implementedBy(i.__class__):
                interfaces.IMetadataStorage(i).setMetaValue(
                    event.key, event.value)
                
    else:
        interfaces.IMetadataStorage(event.item).setMetaValue(
            event.key, event.value)
