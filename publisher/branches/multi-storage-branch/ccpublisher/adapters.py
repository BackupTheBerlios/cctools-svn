import zope.interface

import p6.api
import cctagutils.metadata
import ccpublisher.interfaces

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
