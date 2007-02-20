"""Dispatch to lookup the correct metadata handler for a given file.  Relies
on entry points defined by this package and others to find the correct
handler.  If an appropriate handler is not found for a given file extension,
falls back to XMP extraction.
"""

__id__ = "$Id$"
__version__ = "$Revision$"
__copyright__ = '(c) 2004-2007, Creative Commons, Nathan R. Yergler'
__license__ = 'licensed under the GNU GPL2'

import pkg_resources
from cctagutils.handler.xmp import XmpMetadata
           
def metadata(filename):
    """Returns the appropriate instance for the detected filetype of
    [filename].  The returned instance will be a subclass of the
    AudioMetadata class."""


    # XXX right now we do stupid name-based type detection; a future
    # improvment might actually look at the file's contents or mime/type
    ext = filename.split('.')[-1].lower()
    
    handlers = pkg_resources.iter_entry_points('cctagutils.handler', ext)
    try:
        h = handlers.next()
        return h.load()(filename)

    except StopIteration, e:

        # no file-type specific handler found; fall back to XMP
        return XmpMetadata(filename)
