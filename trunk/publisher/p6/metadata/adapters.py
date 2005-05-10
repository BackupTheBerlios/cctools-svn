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


def collectStorageAppliesTo(event):
    """Checks if the event.item is an interface that the groups we know about
    "appliesTo"; if so, return them."""

    result = [n for n in getattr(p6.api.getApp(), 'storage', [])
              if event.item in zope.interface.implementedBy(n.__class__)]

    return result

def collectRootAppliesTo(event):
    """Checks if the event.item is an interface that the groups we know about
    "appliesTo"; if so, return them."""

    result = [n for n in p6.api.getApp().items
              if event.item in zope.interface.implementedBy(n.__class__)]

    return result

def updateMetadata(event):
    """Reponds to a metadata update event."""

    try:
        interfaces.IMetadataStorage(event.item).setMetaValue(
            event.key, event.value)
    except TypeError, e:
        # look for all items of a particular instance.
        for adapted in zope.component.getGlobalSiteManager().getAdapters(
            (event,), event.item):

            for item in adapted[1]:
                try:
                    interfaces.IMetadataStorage(item).setMetaValue(
                        event.key, event.value)
                except TypeError, e:
                    print "unable to adapt %s" % repr(item)
                    pass
                
        
