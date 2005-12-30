import pyarchive

import zope.interface
import zope.component

import p6
from p6 import api
from p6.metadata.interfaces import IMetadataStorage

class IEmbeddable(zope.interface.Interface):
    pass

class ArchiveStorage(p6.metadata.base.BasicMetadataStorage,
                     p6.storage.basic.BasicStorage):
    zope.interface.implements(p6.metadata.interfaces.IMetadataStorage,
                              p6.storage.interfaces.IStorage)

    # metadata interface
    def __init__(self):
        p6.metadata.base.BasicMetadataStorage.__init__(self)
        p6.storage.basic.BasicStorage.__init__(self)

    def validate(self, event=None):
       # determine the appropriate collection
       work_type = api.findField('format')

       if work_type:
           work_type = work_type.lower()
       else:
           # no work type; can not validate
           raise Exception()

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
       v_url = pyarchive.identifier.verify_url(self.archive_collection,
                                               archive_id,
                                               self.submission_type)
       
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
                   e.embed(license, v_url, year, holder)

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
           sub = submission.addFile(item,
                                    pyarchive.const.ORIGINAL,
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
       archive_URI =  submission.submit(
           IMetadataStorage(self).getMetaValue('username'),
           IMetadataStorage(self).getMetaValue('password'),)

       return {'URI':archive_URI}
       
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
