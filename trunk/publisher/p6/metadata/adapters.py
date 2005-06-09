import zope.interface
import zope.component

import p6
import interfaces
import persistance

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
    print 'in updateMetadata for ', event
    try:
        # store the value locally
        interfaces.IMetadataStorage(event.item).setMetaValue(
            event.field, event.value)

        # check for persistance
        if event.field.persist and event.group.persistMode != 'never': 
            # determine the item identifier
            # (this may need to be revised at some point in the future)
            identifier = persistance.item_id(event.item)
            
            persistance.store(event.field.group().id,
                              event.field.id, event.value)
            
    except TypeError, e:
        # look for all items of a particular instance.
        for adapted in zope.component.getGlobalSiteManager().getAdapters(
            (event,), event.item):

            for item in adapted[1]:
                try:
                    # store the new value
                    interfaces.IMetadataStorage(item).setMetaValue(
                        event.field, event.value)
                    
                    # check for persistance
                    if event.field.persist and \
                           event.group.persistMode != 'never': 
                        # determine the item identifier
                        identifier = persistance.item_id(item)

                        persistance.store(str(event.field.group().id),
                                          str(event.field.id), event.value)

                except TypeError, e:
                    print "unable to adapt %s" % repr(item)
                    pass
                

def loadMetadata(event):
    """Reponds to a metadata load event."""

    try:
        value = persistance.get(str(event.field.group().id),
                                str(event.field.id))
        if value:
            event.value.append(value)
    except KeyError, e:
        pass
    
    
