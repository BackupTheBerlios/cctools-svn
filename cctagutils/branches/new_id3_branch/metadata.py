"""Classes and functions to support embedding metadata in a music file;
contains the abstract class which allows extensions to be implemented for
OGG, etc.
"""

__id__ = "$Id$"
__version__ = "$Revision$"
__copyright__ = '(c) 2004, Creative Commons, Nathan R. Yergler'
__license__ = 'licensed under the GNU GPL2'

import filetypes

meta_handlers = {'mp3':filetypes.mp3.Metadata,
                 }

def createClaimString(year, holder, license, verification=None):
    """Construct a license claim from the constituent pieces suitable for
    embedding."""

    # first generate the embedded license claim str
    claim = "%s %s. Licensed to the public under %s" % (
        year, holder, license )
    
    if verification is not None:
        claim = "%s verify at %s" % (claim, verification)

    return claim

def metadata(filename):
    """Returns the appropriate instance for the detected filetype of
    [filename].  The returned instance will implement interfaces.IMetadata."""

    # XXX right now we do stupid name-based type detection; a future
    # improvment might actually look at the file's contents.
    ext = filename.split('.')[-1].lower()

    try:
        if ext in meta_handlers:
            return meta_handlers[ext].openFile(filename)
        else:
            # return None if we can't find the file in our catalog
            return None
    except IOError, e:
        if getattr(e, 'errno', -1) == 2:
            # file not found -- return None
            return None
        else:
            # re-raise the exception
            raise e
