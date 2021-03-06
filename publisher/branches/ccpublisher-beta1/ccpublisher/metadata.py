import p6
import zope
import zope.interface

def updateMetadataBridge(event):
    """ccPublisher uses properties like title, etc, for the entire work --
    P6 metadata providers publish the information for a particular item.
    This listener looks for fields of interest and republishes the events
    in a way that conforms with ccPublisher's metadata model."""

    FIELDS = ('http://purl.org/dc/elements/1.1/title',)

    if event.canonical in FIELDS and \
           event.item != p6.storage.interfaces.IWork:
        # we care about this field, and we're not consuming our own event
        updateEvent = p6.metadata.events.UpdateMetadataEvent(
            p6.storage.interfaces.IWork,
            event.field,
            event.value,
            )
        zope.component.handle(updateEvent)

def itemSelected(event):
    """IItemSelected event subscriber which provides ID3 metadata for
    MP3 files."""
    
    def group(groupid):
        """Convenience function for finding a metadata group by id."""
        # XXX should this go into p6.api?
        
        return [n for n in p6.api.getApp().groups if
                n.id == groupid][0]

    # make sure a FileItem was selected
    if (p6.storage.interfaces.IFileItem in
        zope.interface.implementedBy(event.item.__class__)):

        print event.item.getIdentifier()
        id3 = metadata(event.item.getIdentifier())
        
        # this is a file item; try to extract ID3
        # XXX this should really update the metadata for this item instead of
        # the work -- would be a more generic solution, but will require
        # handling in the UI
        updateEvent = p6.metadata.events.UpdateMetadataEvent(
            p6.storage.interfaces.IWork,
            group('workinfo'),
            group('workinfo').get('title'),
            id3.getTitle()
            )
        zope.component.handle(updateEvent)

