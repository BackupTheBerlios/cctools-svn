import p6
import p6.ui.pages
from p6.metadata.base import metadatafield, metadatagroup

class StorageDirective(object):
    """A storage declaration."""

    def __init__(self, _context, name, factory):

        app = p6.getApp()
        if getattr(app, 'storage', None) is None:
            app.storage = []

        _context.action(discriminator=None,
                        callable=lambda x: app.storage.append(x()),
                        args=(factory,),
                        )
        
class MGroupDirective(object):
    """A metadata group."""

    def __init__(self, _context, id, title, for_, factory=None):

        self.fields = []
        self.appliesTo = for_
        self.id = id
        self.title = title
        self.factory = factory or metadatagroup

        print 'adding mgroup action...'
        _context.action(discriminator=('MetadataGroup', self.id),
                        callable=self.__addGroup,
                        args=[],
                        )

    def field(self, _context, id, type, label='', choices=[]):
        if label == '':
            label = id

        self.fields.append(
            metadatafield(type)(id, label, choices=choices)
            )

    def __addGroup(self):
        """Add the group to the groups stack once configuration is complete."""
        print self.id
        p6.getApp().groups.append(
            self.factory(self.appliesTo)(self.id, self.title,
                                          self.fields)
            )
        
class PagesDirective(object):
    """Definition of a set of pages."""

    def __init__(self, _context, appid):
        # register the App ID
        p6.getApp().appid = appid

        # initialize the page registry
        p6.getApp().pages = []
        
    def page(self, _context, type_, title=''):
        pass

    def metadatapages(self, _context, for_):
        _context.action(discriminator=('GeneratePages',),
                        callable=self.__generatePages,
                        args=(for_,),
                        )

    def __generatePages(self, for_):
        for page in p6.ui.pages.metadata.generatePages(for_):
            p6.getApp().pages.append(page)
            
    def storepage(self, _context):
        _context.action(discriminator=('RegisterPage', 'StorePage',
                                       p6.ui.pages.StorePage),
                        callable=p6.getApp().pages.append,
                        args=(p6.ui.pages.StorePage,),
                        )

    def xmlpage(self, _context):
        _context.action(discriminator=('RegisterPage', 'XmlDisplayPage',
                                       p6.ui.pages.XmlMetadataPage),
                        callable=p6.getApp().pages.append,
                        args=(p6.ui.pages.XmlMetadataPage,),
                        )


    def xrcpage(self, _context, title, xrcfile, xrcid):
        _context.action(discriminator=('RegisterPage', xrcid,
                                       p6.ui.pages.XrcPage),
                        callable=p6.getApp().pages.append,
                        args=(p6.ui.pages.xrcpage(title, xrcfile, xrcid),),
                        )

    
