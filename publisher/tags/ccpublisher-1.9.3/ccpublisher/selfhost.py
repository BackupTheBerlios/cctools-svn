import os

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

import ui

class CallbackBridge(object):
    """Bridge pyarchive status update callbacks to P6 events."""
    
    def __init__(self):
        pass
    
    def reset(self, steps=1, filename=None, status=''):
        if filename is not None:
            status = 'Uploading %s...' % filename
            steps = os.stat(filename).st_size
            
        resetEvt = p6.ui.events.ResetStatusEvent(steps=steps, message=status)
        zope.component.handle(resetEvt)
        
    def increment(self, status="", steps=1):
        update = p6.ui.events.UpdateStatusEvent(delta=steps,
                                                message=status)
        zope.component.handle(update)
        
    def finish(self):
        pass
    
    def __call__(self, bytes=1):
        self.increment(steps=bytes)
    

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
                   "verification metadata.  In most cases, this will " \
                   "be the page you link to your MP3 file from."
            
            self.__pages.append(
                lambda x: p6.ui.pages.fieldrender.SimpleFieldPage(
                x, 'SELFHOST_UI_META', 'Self Hosted Files', fields,
                self.callback, description=desc))

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

def selfhostStorageFinalPage(storage):

    class SelfHostFinalPage(object):

        zope.interface.implements(p6.ui.interfaces.IPageList)

        def __init__(self, target, event):
            self.__pages = [ui.FinalPage]
            self.__storage = storage

        def __expand(self):
            """Perform last minute string interpolation."""

            if getattr(ui.FinalPage, 'needsExpansion', 'True'):
                # only do this once...
                ui.FinalPage.PAGE_XRC = ui.FinalPage.PAGE_XRC % \
                                        self.__storage.uri
                ui.FinalPage.needsExpansion = False
            
        def list(self):
            # see if we've been activated
            if (self.__storage.activated()):

                self.__expand()
                return self.__pages
            else:
                # not activated, so don't make a contribution to the UI
                return []

    return SelfHostFinalPage

class SelfHostStorage(p6.metadata.base.BasicMetadataStorage,
                     p6.storage.common.CommonStorageMixin):
    
    zope.interface.implements(p6.metadata.interfaces.IMetadataStorage,
                              p6.storage.interfaces.IStorage)

    id = 'SELFHOST_STORAGE'
    name = 'Self-hosted Files'
    description = 'Create metadata suitable for use with files hosted ' \
                  'on your personal web site.'
    
    # metadata interface
    def __init__(self):
        p6.metadata.base.BasicMetadataStorage.__init__(self)

        # register handlers for extension points --
        # this allows us to extend the user interface in a unified way
        # 
        zope.component.provideSubscriptionAdapter(
            selfhostMetadataUi(self),
            (p6.extension.interfaces.IStorageMetaCollection,
             p6.extension.events.IExtensionPageEvent,
             ),
            p6.ui.interfaces.IPageList)

        zope.component.provideSubscriptionAdapter(
            selfhostStorageFinalPage(self),
            (p6.extension.interfaces.IPostStoreExtension,
             p6.extension.events.IExtensionPageEvent,
             ),
            p6.ui.interfaces.IPageList)

    def validate(self, event=None):
       # determine the appropriate collection
       work_type = api.findField('format')

       if work_type:
           work_type = work_type.lower()
       else:
           # no work type; can not validate
           raise KeyError("work_type not specified.")

    def store(self, event=None):
        # generate the RDF
        pass
           
