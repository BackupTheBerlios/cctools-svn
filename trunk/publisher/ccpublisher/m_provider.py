import p6
import zope
import zope.interface

class ID3Provider(object):
    zope.component.adapts(p6.storage.interfaces.IFileItem)
    zope.interface.implements(p6.metadata.interfaces.IMetadataProvider)
    
    def __init__(self, item):
        # store a reference to the item
        # XXX... should this be a weakref?
        self.__item = item
        
    def getMetaValue(self, key):
        """Returns a metadata value.  If the key does not exist, raises a
        KeyError Exception."""

    def keys(self):
        """Returns a sequence of valid metadata keys."""

    def metadata(self):
        """Returns a dictionary-like object containing the key-value pairs
        of metadata defined for this item."""


def itemSelected(event):
    # XXX check for file type here -- dispatch metadata providers?
    def group(groupid):
        return [n for n in p6.api.getApp().groups if
                n.id == groupid][0]
    
    updateEvent = p6.metadata.events.UpdateMetadataEvent(
        p6.storage.interfaces.IWork,
        group('workinfo'),
        group('workinfo').get('title'),
        'testtitle'
        )
    zope.component.handle(updateEvent)

    #print 'in itemSelected(ccp)...', event
    #print p6.api.getApp().items[0]
    #print [i for i in zope.interface.implementedBy(p6.api.getApp().items[0].__class__)]
    
    
# provider ID3Provider as an adapter
#registry = zope.component.getGlobalSiteManager()
#registry.provideAdapter((p6.storage.interfaces.IFileItem,),
#                        p6.metadata.interfaces.IMetadataProvider,
#                        'ID3Provider',
#                        ID3Provider)
