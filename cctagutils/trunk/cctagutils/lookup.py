"""Support functions for verification of embedded license claims."""

__id__ = "$Id$"
__version__ = "$Revision$"
__copyright__ = '(c) 2004, Creative Commons, Nathan R. Yergler'
__license__ = 'licensed under the GNU GPL2'

import ccrdf
import ccrdf.rdfextract as rdfextract
from ccrdf.aaronrdf import cc

import cctagutil
from cctagutils.metadata import metadata

def parseClaim(claim):
    results = {}

    vtext = 'verify at '
    vloc = claim.find(vtext)
    if vloc != -1:
            results['verify at'] = claim[vloc+len(vtext):].strip()
            claim = claim[:vloc]

    ltext = "licensed to the public under "
    lloc = claim.lower().find(ltext)
    if lloc != -1:
            results['license'] = claim[lloc+len(ltext):].strip()
            claim = claim[:lloc]

    results['copyright'] = claim.strip()

    return results

def lookup(filename):
    """Returns True of False if the embedded claim can be verified."""
    
    if verify(filename) > 0:
        return True
    else:
        return False
    
def verify(filename):
    """Extracts license claim information from a file and verifies it.
    Returns the following status codes:
    1     Verified
    0     No RDF
    -1    Work information not found (possible SHA1 mismatch)
    -2    Verification license does not match claim.

    Verification is performed against an embedded "claim" as well as
    checking the page specified by the "web statement".
    """

    status = cctagutil.VERIFY_NO_RDF

    file_metadata = metadata(filename)
    sha1 = 'urn:sha1:%s' % cctag.rdf.fileHash(filename)
    rdf_urls = []
    
    # get the claim URL if available
    claim = file_metadata.getClaim()
    if claim is not None:
    
        fileinfo = parseClaim(claim)
        rdf_urls.append(fileinfo['verify at'])

    # get the web statement URL if available
    if file_metadata.getMetadataUrl():
        rdf_urls.append(file_metadata.getMetadataUrl())

    # parse/extract the metadata
    rdf_store = ccrdf.rdfdict.rdfStore()
    extractor = rdfextract.RdfExtractor()
    for u in rdf_urls:
        extractor.extractUrlToStore(u, rdf_store)

    # look for a license assertion about this file
    license_assertions = rdf_store.store.objects(sha1, cc.license)

    
    # check each block of RDF
    #  (a verification page may also have it's own license RDF embedded)
    for block in verifyRdf:
        # parse/validate the RDF
        verifyCc = ccrdf.ccRdf()
        verifyCc.parse(block)

        # for each work in the RDF block...
        for work in verifyCc.works():
            
            # if the subject matches...
            if work.subject == fileinfo['sha']:
                # we found the work information;
                # only one reason left to not verify
                status = cctagutil.VERIFY_NO_MATCH
                
                # we found the work, now make sure the license matches
                for license in work.licenses():
                    if license == fileinfo['license']:
                        return cctagutil.VERIFY_VERIFIED

    # either the file wasn't found, or the license didn't match
    return status
