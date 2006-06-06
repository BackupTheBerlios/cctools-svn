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

import ui

def selfhostMetadataUi(storage):

    class SelfHostMetadataUi(object):

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

            desc = "Please enter the URL where you will host your " \
                   "verification metadata.  \nIn most cases, this will " \
                   "be the page you link to your MP3 file from."
            
            self.__pages.append(
                lambda x: p6.ui.pages.fieldrender.SimpleFieldPage(
                x, 'SELFHOST_UI_META', 'Self Hosted Files', fields,
                self.callback, description=desc))

            self.__pages.append(
                lambda x: ui.selfhost.FinalPage(x, self.storage)
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
            self.storage.verification_url = value_dict['vurl']
            
            self.storage.registerEvents()

    return SelfHostMetadataUi

class SelfHostStorage(p6.metadata.base.BasicMetadataStorage,
                     p6.storage.common.CommonStorageMixin):
    
    zope.interface.implements(p6.metadata.interfaces.IMetadataStorage,
                              p6.storage.interfaces.IStorage)

    id = 'SELFHOST_STORAGE'
    name = 'Self-hosted Files'
    description = 'Create metadata suitable for use with files hosted ' \
                  'on your web site.'
    
    # metadata interface
    def __init__(self):
        p6.metadata.base.BasicMetadataStorage.__init__(self)

        # register handlers for extension points --
        # this allows us to extend the user interface in a unified way
        # 
        zope.component.provideSubscriptionAdapter(
            selfhostMetadataUi(self),
            (p6.extension.interfaces.IStorageProcessing,
             p6.extension.events.IExtensionPageEvent,
             ),
            p6.ui.interfaces.IPageList)

    def store(self, event=None):
        
        # get the verification URL
        v_url = self.verification_url

        # get the copyright information fields
        license_xml = etree.fromstring(api.getApp().license_doc)
        
        license = api.findField('license', api.getApp().items[0])
        license_name = license_xml.find('license-name').text
        
        year = api.findField('year', api.getApp().items[0])
        holder = api.findField('holder', api.getApp().items[0])

        for item in api.getApp().items:
           # adapt the item to IEmbeddable if possible
           embeddable = zope.component.getGlobalSiteManager().getAdapters(
               [item,], IEmbeddable)

           if embeddable:
               for e in embeddable:
                   # take e[1] since getAdapters returns a list of tuples --
                   # (name, adapter)
                   e[1].embed(license, v_url, year, holder)


        # calculate the hash of each item
        # XXX see triple-x comment in store method of ia.py
        
        self.rdf = cctagutils.rdf.generate_rdfa(
            [n.getIdentifier() for n in api.getApp().items[1:]],
            license_name, license, v_url)
