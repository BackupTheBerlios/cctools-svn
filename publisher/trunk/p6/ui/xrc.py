import os.path

import wx
import wx.xrc

import wraptext

def resource():
    """Create an empty resource and attach custom handlers."""

    xrc_resource = wx.xrc.EmptyXmlResource()
    xrc_resource.InsertHandler(wraptext.WordWrapTextXmlHandler())

    return xrc_resource


def load(filename):
    """Load an XRC resource from a file or an XML fragment specified
    by [filename]; exact behavior is determined by testing if [filename]
    exists."""
    
    xrc_resource = resource()

    if isinstance(filename, (str, unicode)):
        # check if this is a file or an XRC fragment
        if os.path.exists(filename):
            xrc_resource.Load(filename)
        else:
            # we actually have an XRC fragment
            xrc_resource.LoadFromString(filename)

    return xrc_resource

