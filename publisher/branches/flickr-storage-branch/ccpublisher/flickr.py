import os
import elementtree.ElementTree as etree

import pyarchive

import zope.interface
import zope.component

import p6
import p6.ui.events
import p6.storage.common
import p6.extension.exceptions

from p6 import api
from p6.metadata.interfaces import IMetadataStorage
from ccpublisher.interfaces import IEmbeddable
import cctagutils.rdf

from p6.i18n import _

import ui

import ccpublisher.Uploadr as Uploadr

def flickrMetadataUi(storage):

    class flickrMetadataUi(object):

        zope.interface.implements(p6.ui.interfaces.IPageList)

        def __init__(self, target, event):
            self.__pages = None
            self.__storage = storage

        def createPages(self):
            
            # XXX -- hack
            # 
            # We import here because doing so at instantiation causes problems
            # -- in particular, the App needs to be created before other
            # UI objects, and the import has side effects (querying the
            # background color)
            
            import p6.ui.pages.fieldrender
            
            # create the simple page
            fields = [
                p6.metadata.base.metadatafield(p6.metadata.types.ITextField)(
                'vurl', 'Verification URL'),
                ]
            self.__pages = []
            self.__pages.append(
                lambda x: ui.flickr.WarningPage(x, self.storage)
                )
            self.__pages.append(
                lambda x: ui.flickr.FinalPage(x, self.storage)
                )
            
        def list(self):
            # see if we've been activated
            if (self.__storage.activated()):
                
                if self.__pages is None:
                    self.createPages()

                return self.__pages
            else:
                # not activated, so don't ask for information
                return []

        def callback(self, value_dict):

            # make sure the verification URL is specified
            if not( ('vurl' in value_dict) and (value_dict['vurl']) ):
                raise p6.extension.exceptions.ExtensionSettingsException(
                    "You must supply the verification URL.")

            # store the credentials for future use
            #self.storage.verification_url = value_dict['vurl']
            
            self.storage.registerEvents()

    return flickrMetadataUi

class FlickrStorage(p6.metadata.base.BasicMetadataStorage,
                     p6.storage.common.CommonStorageMixin):
    
    id = 'FLICKR_STORAGE'

    # metadata interface
    def __init__(self):
        p6.metadata.base.BasicMetadataStorage.__init__(self)

        # register handlers for extension points --
        # this allows us to extend the user interface in a unified way
        # 
        zope.component.provideSubscriptionAdapter(
            flickrMetadataUi(self),
            (p6.extension.interfaces.IStorageProcessing,
             p6.extension.events.IExtensionPageEvent,
             ),
            p6.ui.interfaces.IPageList)

    def store(self, event=None):       
        # get the verification URL
        v_url = ""
        titlei=api.findField('title')
        descriptioni=api.findField('description')
        #tagsi=api.findField('keywords')
        uploadMe=Uploadr.Uploadr()
        uploadMe.authenticatePt2()
        for item in api.getApp().items[1:]:
           uploadMe.uploadImage(item.getIdentifier(),title=titlei,desc=descriptioni)
