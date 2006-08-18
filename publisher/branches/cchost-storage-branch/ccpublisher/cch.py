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

import ccpublisher
from ccpublisher.interfaces import IEmbeddable
import const

import ui
import pycchost

class CallbackBridge(object):
    """Bridge pyarchive status update callbacks to P6 events."""
    
    def __init__(self):
        # initialize the scale, used to scale progress for very large files
        self.__scale = 1.0
    
    def reset(self, steps=1, filename=None, status=''):
        if filename is not None:
            status = 'Uploading %s...' % filename
            file_size = os.stat(filename).st_size
            
            # scale the file size down
            if file_size > sys.maxint:
                self.__scale = ( (sys.maxint - 1) * 1.0 ) / file_size 
                
            steps = int( file_size * self.__scale )
            
        resetEvt = p6.ui.events.ResetStatusEvent(steps=steps, message=status)
        zope.component.handle(resetEvt)
        
    def increment(self, status="", steps=1):
        update = p6.ui.events.UpdateStatusEvent(delta=steps,
                                                message=status)
        zope.component.handle(update)
        
        
    def finish(self):
        pass
    
    def __call__(self, bytes=1):
        self.increment(steps=int( bytes * self.__scale ))


class CCHostStorageUi(object):

    zope.interface.implements(p6.ui.interfaces.IPageList)

    def __init__(self, storage):
        self.__storage = storage
        self.__pages = None

    def __call__(self, target, event):
        return self

    def createPages(self):

        self.__pages = []
	
	try:
		Request, urlopen = pycchost.loader.loader() # prepare to handle cookies
	except ImportError:
	        raise p6.extension.exceptions.ExtensionSettingsException(
	             _("Failed to import cookielib or ClientCookie. Try to upgrade to python2.4"))
	else:
		self.__storage.Request = Request
		self.__storage.urlopen = urlopen

        self.__pages.append(lambda x: ui.cch.CCHostLocationPage(x,self.__storage))
        self.__pages.append(lambda x: ui.cch.CCHostLoginPage(x,self.__storage))
        self.__pages.append(lambda x: ui.cch.CCHostSubmissionTypePage(x,self.__storage))
        self.__pages.append(lambda x: ui.cch.CCHostFormSubmission(x,self.__storage))        
	self.__pages.append(p6.ui.pages.StorePage)
        self.__pages.append(lambda x: ui.cch.CCHostFinalPage(x, self.__storage))

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
	# set the upload results
	self.uploads = [] 
	self.firstCall = True
	print "init"
        
        # register handlers for extension points --
        # this allows us to extend the user interface in a unified way
        # 
        zope.component.provideSubscriptionAdapter(
            CCHostStorageUi(self),
            (p6.extension.interfaces.IStorageProcessing,
             p6.extension.events.IExtensionPageEvent,
             ),
            p6.ui.interfaces.IPageList)

    def validate(self, event=None):
	pass

    def store(self, event=None):
	if self.firstCall:
		self.firstCall = False
		callback = CallbackBridge()
		for item in p6.api.getApp().items[1:]:
			pathfile = item.getIdentifier()
			filepath, filename = os.path.split(pathfile)
			# upload each file
			self.uploads.append(self.uploadFiles(filename, pathfile, callback))
    
    def uploadFiles(self, filename, pathfile, callback):
	file = [] # (name, filename, value)
	file.append(("upload_file_name", self.file_name, lambda: open(pathfile, 'rb').read()))
	try:
		# reset the gauge for this file
		callback.reset(filename=pathfile)
		htmlSource = pycchost.upload.post_multipart(self.submissionlink, self.values, file, self.urlopen, self.Request)
	except IOError, e:
    		callback.increment(status="Failed to open the URL.\nThis usually means the server doesn't exist, is down, or we don't have an internet connection.")
		return False, None, "Failed to connect to the server"
	else:
		p = pycchost.upload.uploadParser() # verify if upload succeeded
	        p.feed(htmlSource)
	        p.close()
		if p.uploadSucceeded:
			callback.increment(status="File %s uploaded" % filename)
		else:
			callback.increment(status="Failed to upload %s" % filename)
	
		return p.uploadSucceeded, p.url, p.error

