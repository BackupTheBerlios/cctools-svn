"""
  p6.app.bananas
  ==============
  
  Monkey-patch methods for P6.  These methods and functions are injected
  into vendor-supplied code to override default behavior so it fits our
  needs.
  
"""

import errno
import os

def openInOrPlain(filename):
    """Open a file, falling back to filename.in.

    If the requested file does not exist and filename.in does, fall
    back to filename.in.  If opening the original filename fails for
    any other reason, allow the failure to propogate.

    For example, the tests/samplepackage dirextory has files:

       configure.zcml
       configure.zcml.in
       foo.zcml.in

    If we open configure.zcml, we'll get that file:

    >>> here = os.path.dirname(__file__)
    >>> path = os.path.join(here, 'tests', 'samplepackage', 'configure.zcml')
    >>> f = openInOrPlain(path)
    >>> f.name[-14:]
    'configure.zcml'

    But if we open foo.zcml, we'll get foo.zcml.in, since there isn't a
    foo.zcml:

    >>> path = os.path.join(here, 'tests', 'samplepackage', 'foo.zcml')
    >>> f = openInOrPlain(path)
    >>> f.name[-11:]
    'foo.zcml.in'

    Make sure other IOErrors are re-raised.  We need to do this in a
    try-except block because different errors are raised on Windows and
    on Linux.

    >>> try:
    ...     f = openInOrPlain('.')
    ... except IOError:
    ...     print "passed"
    ... else:
    ...     print "failed"
    ...
    passed

    """
    
    try:
        fp = open(filename)
    except IOError, (code, msg):
        if code == errno.ENOENT:
            fn = filename + ".in"
            lib_pos = filename.find('library.zip')
            if lib_pos > 0:
                sxs_fn = filename[:lib_pos] + filename[lib_pos+12:]
            else:
                sxs_fn = filename
            
            if os.path.exists(fn):
                fp = open(fn)
            elif os.path.exists(sxs_fn):
                # try to open it as part of a py2exe side-by-side
                fp = open(sxs_fn)
            else:
                raise
        else:
            raise
    return fp

