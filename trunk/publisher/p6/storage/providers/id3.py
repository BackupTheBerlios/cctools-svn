import p6
import zope.interface

from cctagutils.metadata import metadata

def itemSelected(event):
    """IItemSelected event subscriber which provides ID3 metadata for
    MP3 files."""
    
    # make sure a FileItem was selected
    if (p6.storage.interfaces.IFileItem in
        zope.interface.implementedBy(event.item.__class__)):

        try:
            id3 = metadata(event.item.getIdentifier())

            # this is a file item; try to extract ID3
            updateEvent = p6.metadata.events.UpdateMetadataEvent(
                event.item,
                'http://purl.org/dc/elements/1.1/title',
                id3.getTitle()
                )
            zope.component.handle(updateEvent)

        except NotImplementedError, e:
            """NotImplementedError simply indicates the cctagutils metadata
            framework can not extract the field; nothing to see here, move
            along."""
            
            return
        
