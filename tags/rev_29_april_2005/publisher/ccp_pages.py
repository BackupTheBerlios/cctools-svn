import zope.interface
import ccwx.xrcwiz

import p6.ui.interfaces
import p6.ui.pages

import p6.metadata
import p6.metadata.types as metatypes
import p6.storage

from p6.metadata.base import metadatafield, MetadataGroup

def metafields():
    return [MetadataGroup('itemmeta',
                          fields=[
        metadatafield(p6.metadata.types.ITextField)('bar', 'bar'),
        metadatafield(p6.metadata.types.ISelectionField)('b','xyz',
                                                    choices=['a','b','c']),],
                          appliesTo=p6.storage.interfaces.IWork),
            MetadataGroup('workmeta',
                          fields=[
        metadatafield(metatypes.ITextField)('foo', 'foo'),],
                          appliesTo=p6.storage.interfaces.IWorkItem),
            p6.metadata.license.LicenseGroup('licenseinfo',
                                fields=[
        metadatafield(metatypes.ITextField)('license','license'),],
                                appliesTo=p6.storage.interfaces.IWork),
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
    
