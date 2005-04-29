import zope.interface
import ccwx.xrcwiz

import p6.ui.interfaces
import p6.ui.pages

import p6.metadata
import p6.metadata.types as metatypes
import p6.storage

from p6.metadata.base import metadatafield, metadatagroup

def metafields():
    return [metadatagroup(p6.storage.interfaces.IWork)('itemmeta',
                          fields=[
        metadatafield(p6.metadata.types.ITextField)('bar', 'bar'),
        metadatafield(p6.metadata.types.ISelectionField)('b','xyz',
                                                    choices=['a','b','c']),],),
        metadatagroup(p6.storage.interfaces.IWorkItem)('workmeta',
                          fields=[
        metadatafield(metatypes.ITextField)('foo', 'foo'),],),
            p6.metadata.license.LicenseGroup('licenseinfo',
                                fields=[
        metadatafield(metatypes.ITextField)('license','license'),]),
            ]
        
def all_pages(frame):
    """Returns a list of the pages for the application."""
    return [ccwx.xrcwiz.XrcWizPage(frame.getPageParent(),
                                   frame.app.xrcfile,
                                   'CCTAG_WELCOME',
                                   'Welcome'),
            p6.ui.pages.FileSelectorPage(frame),
            ] + \
            p6.ui.pages.metadata.generatePages(frame) + \
            [p6.ui.pages.StorePage(frame),
             p6.ui.pages.XmlMetadataPage(frame),
             ]
    
