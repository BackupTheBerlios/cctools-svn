import os
import sys
import socket

import pycchost

import zope.interface
import zope.component

import p6
import p6.ui.events
import p6.ui.pages
import p6.storage.common
import p6.extension.exceptions

from p6 import api
from p6.metadata.interfaces import IMetadataStorage
import p6.metadata.persistance
from p6.i18n import _

from ccpublisher.interfaces import IEmbeddable
import const

import ui
import pycchost

class CCHostStorageUi(object):

    zope.interface.implements(p6.ui.interfaces.IPageList)

    def __init__(self, storage):
        self.__storage = storage
        self.__pages = None

    def __call__(self, target, event):
        return self

    def createPages(self):

        self.__pages = []

	Request, urlopen = pycchost.loader.loader() # prepare to handle cookies
	self.__storage.Request = Request
	self.__storage.urlopen = urlopen

        self.__pages.append(lambda x: ui.cch.CCHostLocationPage(x,self.__storage))
        self.__pages.append(lambda x: ui.cch.CCHostLoginPage(x,self.__storage))
        self.__pages.append(lambda x: ui.cch.CCHostSubmissionTypePage(x,self.__storage))
#        self.__pages.append(lambda x: ui.cch.CCHostFormSubmission (x,self.__storage))        
        self.__pages.append(p6.ui.pages.StorePage)
#        self.__pages.append(lambda x: ui.cch.CCHostFinalPage(x, self.__storage))

    def list(self):
        # see if we've been activated
        if (self.__storage.activated()):

            if self.__pages is None:
                self.createPages()

            return self.__pages
        else:
            # not activated, so don't ask for information
            return []

class CCHostStorage(p6.metadata.base.BasicMetadataStorage,
                     p6.storage.common.CommonStorageMixin):
    
    zope.interface.implements(p6.metadata.interfaces.IMetadataStorage,
                              p6.storage.interfaces.IStorage)

    id = 'CCHOST_STORAGE'
    
    # metadata interface
    def __init__(self):
        p6.metadata.base.BasicMetadataStorage.__init__(self)

        # set the default identifier and resulting uri
        self.identifier = None
        self.uri = ''
        
        # register handlers for extension points --
        # this allows us to extend the user interface in a unified way
        # 
        zope.component.provideSubscriptionAdapter(
            CCHostStorageUi(self),
            (p6.extension.interfaces.IStorageProcessing,
             p6.extension.events.IExtensionPageEvent,
             ),
            p6.ui.interfaces.IPageList)
 