import p6
import p6.api

from p6.metadata.base import metadatafield, MetadataGroup

class StorageDirective(object):
    """A storage declaration."""

    def __init__(self, _context, name, factory):

        app = p6.api.getApp()
        if getattr(app, 'storage', None) is None:
            app.storage = []

        _context.action(discriminator=None,
                        callable=lambda x: app.storage.append(x()),
                        args=(factory,),
                        )
        
class MGroupDirective(object):
    """A metadata group."""

    def __init__(self, _context, id, title, for_,
                 description='', factory=None):

        self.fields = []
        self.appliesTo = for_
        self.id = id
        self.title = title
        self.factory = factory or MetadataGroup
        self.description = description

        _context.action(discriminator=('MetadataGroup', self.id),
                        callable=self.__addGroup,
                        args=[],
                        )

    def field(self, _context, id, type,
              label='', choices=[], description='', tip=''):
        if label == '':
            label = id

        self.fields.append(
            metadatafield(type)(id, label, choices=choices,
                                description=description, tip=tip)
            )

    def __addGroup(self):
        """Add the group to the groups stack once configuration is complete."""
        p6.api.getApp().groups.append(
            self.factory(self.id, self.appliesTo, self.title,
                         description = self.description,
                         fields = self.fields)
            )
        
class PagesDirective(object):
    """Definition of a set of pages."""

    def __init__(self, _context, appid):
        # register the App ID
        p6.api.getApp().appid = appid

        # initialize the page registry
        p6.api.getApp().pages = []
        
    def page(self, _context, type_, title=''):
        pass

    def metadatapages(self, _context, for_):
        _context.action(discriminator=('GeneratePages',),
                        callable=self.__generatePages,
                        args=(for_,),
                        )

    def __generatePages(self, for_):
        for page in p6.ui.pages.metadata.generatePages(for_):
            p6.api.getApp().pages.append(page)
            
    def storepage(self, _context):
        _context.action(discriminator=('RegisterPage', 'StorePage',
                                       p6.ui.pages.StorePage),
                        callable=p6.api.getApp().pages.append,
                        args=(p6.ui.pages.StorePage,),
                        )

    def fileselector(self, _context):
        _context.action(discriminator=('RegisterPage', 'FileSelector'),
                        callable=p6.api.getApp().pages.append,
                        args=(p6.ui.pages.FileSelectorPage,),
                        )

    def xmlpage(self, _context):
        _context.action(discriminator=('RegisterPage', 'XmlDisplayPage',
                                       p6.ui.pages.XmlMetadataPage),
                        callable=p6.api.getApp().pages.append,
                        args=(p6.ui.pages.XmlMetadataPage,),
                        )


    def xrcpage(self, _context, title, xrcfile, xrcid):
        _context.action(discriminator=('RegisterPage', xrcid,
                                       p6.ui.pages.XrcPage),
                        callable=p6.api.getApp().pages.append,
                        args=(p6.ui.pages.xrcpage(title, xrcfile, xrcid),),
                        )

    
