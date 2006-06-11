import zope.interface
import zope.component

import p6.ui.interfaces
import events

def target(target_interface):
    class ExtensionPointTarget(object):
        zope.interface.implements(target_interface)

    return ExtensionPointTarget()

class ExtensionPoint(object):

    def __init__(self, for_):
        """Instantiate an extension point for the specified interface, for_."""

        self.__for = for_

    def __call__(self, parent):
        self.__parent = parent
        
        return self
    
    def implementors(self):
        """Return the list of pages for this extension point."""

        # XXX create an event and publish it here
        event = events.ExtensionPageEvent()
        print 'in extensionpoint.pages'
        print self.__for

        subs = zope.component.subscribers( (target(self.__for), event),
                                           p6.ui.interfaces.IPageList )

        print 'returning page sets:'
        print  [n.list() for n in subs if n is not None]
        
        return [n.list() for n in subs if n is not None]

## class ExtensionPointTarget(object):
##     def __init__(self, interface):
##         zope.interface.directlyImplements(self, interface)

        
## class activatedStorageExtension(object):
##     zope.interface.implements(interfaces.IExtensionPoint)

##     def __init__(self, iTarget):
##         self.__target = iTarget


##     def call(self):
##         targetObj = ExtensionPointTarget(self.__target)
##         result = []
        
##         for n in p6.api.getApp().storage:

##             if interfaces.IActivated in zope.interface.implementedBy(n):
##                 # this object is activated
##                 a = zope.component.queryMultiAdapter( (n, targetObj),
##                                                       IPageList )

##                 if a:
##                     result.append(a(n, targetObj))

##         return result
