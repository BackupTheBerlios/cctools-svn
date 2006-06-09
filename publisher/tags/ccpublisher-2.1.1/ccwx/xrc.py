import wx
import wx.xrc

import wraptext

def resource():
    """Create an empty resource and attach custom handlers."""

    xrc_resource = wx.xrc.EmptyXmlResource()
    xrc_resource.InsertHandler(wraptext.WordWrapTextXmlHandler())

    return xrc_resource


def load(filename):
    """Load the XRC resource specified by filename and return it."""

    xrc_resource = resource()
    xrc_resource.Load(filename)

    return xrc_resource

