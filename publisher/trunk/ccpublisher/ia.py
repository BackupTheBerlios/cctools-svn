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
    

def archiveStorageUi(storage):

    class ArchiveStorageUi(object):

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
                'username', 'Username'),
                p6.metadata.base.metadatafield(p6.metadata.types.IPasswordField)(
                'password', 'Password'),
                ]

            self.__pages = []
            
            self.__pages.append(
                lambda x: p6.ui.pages.fieldrender.SimpleFieldPage(
                x, 'ARCHIVE_UI_META', 'Internet Archive', fields,
                self.callback))

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

            # make sure both a username and password were provided
            if not('username' in value_dict and 'password' in value_dict):
                raise p6.extension.exceptions.ExtensionSettingsException(
                    "You must supply both a username and password.")
            
            # validate the credentials with IA
            if not(pyarchive.user.validate(value_dict['username'],
                                           value_dict['password'])):

                raise p6.extension.exceptions.ExtensionSettingsException(
                    "Invalid username or password.")

            # store the credentials for future use
            self.storage.credentials = (value_dict['username'],
                                        value_dict['password'])

            # register for future storage events after validating our
            # storage-specific settings
            
            self.storage.registerEvents()

    return ArchiveStorageUi

def archiveStorageFinalPage(storage):

    class ArchiveStorageUi(object):

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

    return ArchiveStorageUi

class ArchiveStorage(p6.metadata.base.BasicMetadataStorage,
                     p6.storage.common.CommonStorageMixin):
    
    zope.interface.implements(p6.metadata.interfaces.IMetadataStorage,
                              p6.storage.interfaces.IStorage)

    id = 'ARCHIVE_STORAGE'
    name = 'Internet Archive Storage'
    description = 'Upload works to the Internet Archive (www.archive.org).'
    
    # metadata interface
    def __init__(self):
        p6.metadata.base.BasicMetadataStorage.__init__(self)

        # register handlers for extension points --
        # this allows us to extend the user interface in a unified way
        # 
        zope.component.provideSubscriptionAdapter(
            archiveStorageUi(self),
            (p6.extension.interfaces.IStorageMetaCollection,
             p6.extension.events.IExtensionPageEvent,
             ),
            p6.ui.interfaces.IPageList)

        zope.component.provideSubscriptionAdapter(
            archiveStorageFinalPage(self),
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
       # generate the identifier and make sure it's available
       archive_id = self.__archiveId()

       # generate the verification url
       v_url = pyarchive.identifier.verify_url(archive_id)
       
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
           archive_id,
           self.archive_collection,
           self.submission_type,
           api.findField('title')
           )

       # retrieve all metadata fields for the work (the root item)
       root_item = api.getApp().items[0]
       for g in api.getApp().groups:
           meta_dicts = [p6.metadata.interfaces.IMetadataStorage(root_item)]
           
           for m in meta_dicts:
               for k in m.keys():
                   submission[k] = m.getMetaValue(k)


       # now add the individual files to the submission
       for item in p6.api.getApp().items[1:]:
           # XXX we're passing in the filename instead of the item and this is really, really bad
           # XXX we should make pyarchive interface aware, give it it's own InputItem interface
           # XXX and then adapt our item to that.
           sub = submission.addFile(item.getIdentifier(),
                                    pyarchive.const.ORIGINAL,
                                    format = p6.metadata.interfaces.IMetadataProvider(item).getMetaValue("format"),
                                    claim = self.__claimString(license,
                                                               v_url,
                                                               year,
                                                               holder)
                                    )
           
           for g in p6.api.getApp().groups:
               meta_dicts = [p6.metadata.interfaces.IMetadataStorage(item)]

               for m in meta_dicts:
                   for k in m.keys():
                       print 'setting %s to %s...' % (k, m.getMetaValue(k))
                       setattr(item, k, m.getMetaValue(k) or '')

       print submission.metaxml().getvalue()
       print submission.filesxml().getvalue()
       
       self.uri = submission.submit(
           self.credentials[0], self.credentials[1],
           callback=CallbackBridge())

       return {'URI':self.uri}
       
    def __archiveId(self):
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


"""
   def archive(self, event):

       for filename in self._files:
           sub = submission.addFile(filename, pyarchive.const.ORIGINAL,
                              claim = self.__claimString(license, v_url, year, holder)
                              )
           sub.format = self.getPage('FILE_FORMAT').getFormat(filename)

       final_url = submission.submit(XRCCTRL(self, "TXT_USERNAME").GetValue(),
                         XRCCTRL(self, "TXT_PASSWORD").GetValue(),
                         callback=XRCCTRL(self, "FTP_PROGRESS").callback)

       return final_url
"""
