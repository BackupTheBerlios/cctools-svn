import wx

import zope.interface

import metadata
import ui
import storage
import configure

def deinstify(func):
    def foo(*args, **kwargs):
        func(*args, **kwargs)
        
    return foo

def nearest(items, target):
    if len(items) == 1:
        return items[0]

    for n in items:
        print zope.interface.implementedBy(n.__class__)

    return items[-1]

def getApp():
    return wx.GetApp()
