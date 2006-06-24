import os
import sys
import socket

import pyarchive

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
    

class ArchiveStorageUi(object):

    zope.interface.implements(p6.ui.interfaces.IPageList)

    def __init__(self, storage):
        self.__storage = storage
        self.__pages = None

    def __call__(self, target, event):
        return self

    def createPages(self):

        self.__pages = []

        self.__pages.append(lambda x: ui.ia.IdentifierPage(x,
                                                           self.__storage))
        self.__pages.append(lambda x: ui.ia.ArchiveLoginPage(x,
                                                           self.__storage))
        self.__pages.append(p6.ui.pages.StorePage)
        self.__pages.append(lambda x: ui.ia.FinalPage(x, self.__storage))

    def list(self):
        # see if we've been activated
        if (self.__storage.activated()):

            if self.__pages is None:
                self.createPages()

            return self.__pages
        else:
            # not activated, so don't ask for information
            return []


class ArchiveStorage(p6.metadata.base.BasicMetadataStorage,
                     p6.storage.common.CommonStorageMixin):
    
    zope.interface.implements(p6.metadata.interfaces.IMetadataStorage,
                              p6.storage.interfaces.IStorage)

    id = 'ARCHIVE_STORAGE'
    
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
            ArchiveStorageUi(self),
            (p6.extension.interfaces.IStorageProcessing,
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

       if work_type == 'audio':
           self.archive_collection = pyarchive.const.OPENSOURCE_AUDIO
           self.submission_type = pyarchive.const.AUDIO
       elif work_type == 'video':
           self.archive_collection = pyarchive.const.OPENSOURCE_MOVIES
           self.submission_type = pyarchive.const.VIDEO
       else:
           self.archive_collection = pyarchive.const.OPENSOURCE_MEDIA
           self.submission_type = work_type = api.findField('format')

    def store(self, event=None):
       # generate the verification url
       v_url = pyarchive.identifier.verify_url(self.identifier)
       
       # get the copyright information fields
       license = api.findField('license', api.getApp().items[0])

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

       # create the submission object
       submission = pyarchive.submission.ArchiveItem(
           pyarchive.submission.UploadApplication("ccPublisher",
                                                  const.version())
           )
       
       # set the submission identifier, collection, etc
       submission.identifier = self.identifier
       submission.collection = self.archive_collection
       submission.mediatype = self.submission_type
       submission.title = api.findField('title')
       submission['licenseurl'] = license
       
       # retrieve all metadata fields for the work (the root item)
       root_item = api.getApp().items[0]
       for g in api.getApp().groups:
           meta_dicts = [p6.metadata.interfaces.IMetadataStorage(root_item)]
           
           for m in meta_dicts:
               for k in m.keys():
                   submission[k] = m.getMetaValue(k)


       # now add the individual files to the submission
       for item in p6.api.getApp().items[1:]:
           # XXX we're passing in the filename instead of the item
           # XXX and this is really, really bad
           # XXX we should make pyarchive interface aware, give it
           # XXX it's own InputItem interface
           # XXX and then adapt our item to that.
           
           try:
               sub = submission.addFile(item.getIdentifier(),
                                        pyarchive.const.ORIGINAL,
                                        format = p6.metadata.interfaces.IMetadataProvider(item).getMetaValue("format"),
                                        claim = self.__claimString(license,
                                                                   v_url,
                                                                   year,
                                                                   holder)
                                        )
           except IOError, e:
               # the file doesn't exist
               p6.api.showError(_("The selected file %s can not be found."))

               sys.exit(2)
           
           for g in p6.api.getApp().groups:
               meta_dicts = [p6.metadata.interfaces.IMetadataStorage(item)]

               for m in meta_dicts:
                   for k in m.keys():
                       print 'setting %s to %s...' % (k, m.getMetaValue(k))
                       setattr(item, k, m.getMetaValue(k) or '')

       print submission.metaxml().getvalue()
       print submission.filesxml().getvalue()

       try:
           self.uri = submission.submit(
               self.credentials[0], self.credentials[1],
               callback=CallbackBridge())
       except IOError, e:
           if getattr(e, 'errno', -1) == 13:
               # permission denied
               p6.api.showError(_("ccPublisher does not have sufficient permissions to read the selected files."))
               
               sys.exit(2)
               
       return {'URI':self.uri}
       
    def defaultIdentifier(self):
        """Generates an archive.org identifier from work metadata or
        embedded ID3 tags."""

        id_pieces = []
        creator = api.findField('holder')
        if creator:
           id_pieces.append(creator)

        title = api.findField('title')
        if title:
           id_pieces.append(title)

        archive_id = pyarchive.identifier.munge(" ".join(id_pieces))
        try:
           id_avail = pyarchive.identifier.available(archive_id)
        except pyarchive.exceptions.MissingParameterException, e:
           id_avail = False

        # if the id is not available, add a number to the end
        # and check again
        i = 0
        orig_id = archive_id
        while not(id_avail):
           archive_id = '%s_%s' % (orig_id, i)

           i = i + 1
           id_avail = pyarchive.identifier.available(archive_id)

        return archive_id

    def __claimString(self, license, verification, year, holder):
        return "%s %s. Licensed to the public under %s verify at %s" % (
            year, holder, license, verification )

