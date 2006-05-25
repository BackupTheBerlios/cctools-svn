"""Generic page which collects the metadata values entered and displays
a rough XML-ish representation."""

import wx
from wx.xrc import XRCCTRL
import ccwx

import zope.interface
import zope.component

import p6
import p6.metadata

class XmlMetadataPage(ccwx.xrcwiz.XrcWizPage):
    """Collects all the metadata fields and displays them as XML."""
    
    
    XRCID = "XML_META"

    def __init__(self, parent, headline='Metadata as XML'):
        ccwx.xrcwiz.XrcWizPage.__init__(self, parent,
                                        os.path.join(p6.api.getResourceDir(),
                                                     "p6.xrc"),
                                        "XML_META",
                                        headline)

    def onChanged(self, event):
        event = p6.metadata.events.CollectGroups(None)
        zope.component.handle(event)

        xml_strings = []
        for group in event.getGroups():
            xml_strings = xml_strings + \
                zope.component.getGlobalSiteManager().getAdapters(
                [group], p6.metadata.interfaces.IXmlString)

        XRCCTRL(self, "TXT_XML").SetValue("\n".join([n[1] for n in xml_strings]))
    
