"""
Adapters for determining the metadata values as they apply to specific
interfaces and objects.
"""

import zope.interface
import zope.component

import p6
import interfaces
import persistance

def groupToXml(metaGroup):
    """
    Converts a Metadata Group to an XML string.
    
    @deprecated: This supported an earlier prototype; it may be revived to
        support 3rd party extensions.
    """
    
    if metaGroup.appliesTo is not None:
        # != p6.storage.interfaces.IWork:
        elements = "\n".join(["<%s>%s</%s>" % (n.id, n(), n.id) for n in
                   metaGroup.getFields()])
        return "<%s>\n%s\n</%s>" % (metaGroup.id, elements, metaGroup.id)
    else:
        return None


def collectStorageAppliesTo(event):
    """Adapts an IUpdateMetadataEvent to a particular interface, returning
    a list of Storage which implement that interface.  Used for updating
    metadata when we know the interface, but not instance we want to apply
    the value to.

    @param event: the event object to handle
    @type event: object implementing L{p6.metadata.events.IUpdateMetadataEvent}

    @return: a list of Storages which implement the interface
        specified by event.item
    @rtype: sequence
    """

    result = [n for n in getattr(p6.api.getApp(), 'storage', [])
              if event.item in zope.interface.implementedBy(n.__class__)]

    return result

def collectRootAppliesTo(event):
    """Adapts an IUpdateMetadataEvent to a particular interface, returning
    a list of Items which implement that interface.  Used for updating
    metadata when we know the interface, but not instance we want to apply
    the value to.

    @param event: the event object to handle
    @type event: object implementing L{p6.metadata.events.IUpdateMetadataEvent}

    @return: a list of Items which implement the interface
        specified by event.item
    @rtype: sequence
    """

    result = [n for n in p6.api.getApp().items
              if event.item in zope.interface.implementedBy(n.__class__)]

    return result

def updateMetadata(event):
    """Event handler for L{p6.metadata.events.IUpdateMetadataEvent}.  Attempts
    to adapt the event's item to IMetadataStorage and set the value.  If the
    field is flagged for persistant storage, it's value is stored.

    @param event: the event object to handle
    @type event: object implementing L{p6.metadata.events.IUpdateMetadataEvent}
    """

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
    """Event handler for L{p6.metadata.events.ILoadMetadataEvent}.  Attempts
    to load the value for the field from persistant storage.

    @param event: the event object to handle
    @type event: object implementing L{p6.metadata.events.ILoadMetadataEvent}
    """

    try:
        value = persistance.get(str(event.field.group().id),
                                str(event.field.id))
        if value:
            event.value.append(value)
    except KeyError, e:
        pass
    
    
