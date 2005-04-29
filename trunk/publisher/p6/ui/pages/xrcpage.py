import wx
from wx.xrc import XRCCTRL
import ccwx

import zope.interface
import zope.component

import p6
import p6.metadata

class XrcPage(ccwx.xrcwiz.XrcWizPage):

    def __init__(self, parent, headline, xrcfile, xrcid):
        ccwx.xrcwiz.XrcWizPage.__init__(self, parent,
                                        xrcfile, xrcid, headline)


def xrcpage(title, xrcfile, xrcid):
    return lambda x: XrcPage(x, title, xrcfile, xrcid)
