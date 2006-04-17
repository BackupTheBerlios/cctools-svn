import wx
import zope.interface
import zope.component

import p6.api
import p6.storage.interfaces
import p6.metadata.events

import cctagutils.metadata
import ccpublisher.interfaces

MIME_MANAGER = wx.MimeTypesManager()

def workFormatListener(event):
    """Subscriber for IItemSelected events; attempts to determine the overall
    work format from the file extension or mime-type.  If possible, publishes
    an UpdateMetadata event."""

    # check if this is a file item (the only type we know how to handle)
    if p6.storage.interfaces.IFileItem in \
           zope.interface.providedBy(event.item):

        file_info = MIME_MANAGER.GetFileTypeFromExtension(
            event.item.filename.split(".")[-1])
        mime_type = file_info.GetMimeType()
        
        # check if this falls into one of our types
        
        if ("text" in mime_type):
            type_value = "Text"
        elif ("audio" in mime_type):
            type_value = "Audio"
        elif ("video" in mime_type):
            type_value = "Video"
        elif ("image" in mime_type):
            type_value = "Image"
        else:
            # fall back to "Other" as the default if we can't figure it out
            type_value = "Other"
        
        updateEvent = p6.metadata.events.UpdateMetadataEvent(
            event.item,
            "http://purl.org/dc/elements/1.1/type",
            type_value)
        
        zope.component.handle(updateEvent)
    
class CcTagUtilsEmbeddable(object):
    zope.interface.implements(ccpublisher.interfaces.IEmbeddable)

    def __init__(self, fileItem):
        self.item = fileItem

    def embed(self, license, v_url, year, holder):
        filename = self.item.getIdentifier()

        # check if we can get an embedding handle
        mdata = cctagutils.metadata.metadata(filename)

        if mdata is None:
            # cctagutils doesn't support this file type, do nothing
            return

        # see if we can write to the file
        if not(mdata.isWritable()): return

        # embed the claim, license url and verification url
        mdata.setClaim(
            cctagutils.metadata.createClaimString(year, holder,
                                                  license, v_url)
            )

        mdata.setLicenseUrl(license)
        mdata.setMetadataUrl(v_url)
