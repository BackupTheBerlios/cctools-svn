import zope.component

import p6
import p6.api

from p6.metadata.base import metadatafield, MetadataGroup

class ExtensionDirective(object):
    """extension registration."""

    def __init__(self, _context, id, name, description='', locale='locale'):

        _context.action(discriminator=('extension', 'i18n_path', id),
                        callable=p6.i18n.addCatalogPath,
                        args=(_context.path(locale),),
                        )

        _context.action(discriminator=('extension', 'i18n_domain', id),
                        callable=p6.i18n.loadCatalog,
                        args=(_context.i18n_domain,),
                        )
        
class StorageDirective(object):
    """A storage declaration."""

    def __init__(self, _context, id, name, factory, description=''):

        # we construct a lambda here since the registry won't actually be
        # instantiated until the entire application is configured
        deferred_lookup = lambda w,x,y,z: zope.component.getUtility(
            p6.storage.registry.IStorageRegistry).register(w,x,y,z)
        
        _context.action(discriminator=('storage', name, ),
                        callable=deferred_lookup,
                        args=(id, name, factory, description),
                        )
        
class MGroupDirective(object):
    """A metadata group."""

    def __init__(self, _context, id, title, for_,
                 description='', factory=None, persistMode='always'):

        self.fields = []
        self.appliesTo = for_
        self.id = id
        self.title = title
        self.factory = factory or MetadataGroup
        self.description = description
        self.persistMode = persistMode

        if persistMode not in ('always', 'never', 'prompt'):
            # not a valid value; throw an error.
            raise ValueError("Invalid value for persistMode.")
        
        _context.action(discriminator=('MetadataGroup', self.id),
                        callable=self.__addGroup,
                        args=[],
                        )

    def field(self, _context, id, type,
              label='', choices=[], choicesList=None, description='',
              tip='', validator=None, persist=False,
              canonical=''):
        if label == '':
            label = id

        if choicesList:
            choicesList = list(choicesList)
            choicesList.sort()
        
        self.fields.append(
            metadatafield(type)(id, label, choices=(choicesList or choices),
                                description=description, tip=tip,
                                validator=validator, persist=persist,
                                canonical=canonical)
            )

    def __addGroup(self):
        """Add the group to the groups stack once configuration is complete."""
        p6.api.getApp().groups.append(
            self.factory(self.id, self.appliesTo, self.title,
                         description = self.description,
                         fields = self.fields,
                         persistMode = self.persistMode)
            )
        
class PagesDirective(object):
    """Definition of a set of pages."""

    def __init__(self, _context, appid):
        p6_app = p6.api.getApp()

        if p6_app is not None:
            # really running the app...
            self.__running = True
            
            # register the App ID
            p6_app.appid = appid

            # initialize the page registry
            p6_app.pages = []

        else:
            self.__running = False
        
    def metadatapages(self, _context, for_):
        _context.action(discriminator=('GeneratePages',),
                        callable=self.__generatePages,
                        args=(for_,),
                        )

    def __generatePages(self, for_):
        # XXX use an anonymous function so we don't generate pages until
        # after all the extension code has loaded

        pagegen = lambda x: p6.ui.pages.metadata.generatePages(for_)
        pagegen.expand = True

        if self.__running:
            p6.api.getApp().pages.append(pagegen)

    def storageSelector(self, _context):
        if self.__running:
            _context.action(discriminator=('RegisterPage', 'StorageSelector',
                                           p6.ui.pages.StorageSelectorPage),
                            callable=p6.api.getApp().pages.append,
                            args=(p6.ui.pages.StorageSelectorPage,),
                            )

    def finalUrl(self, _context, title):
        if self.__running:
            _context.action(discriminator=('RegisterPage', 'FinalUrlPage',
                                           p6.ui.pages.StorePage),
                            callable=p6.api.getApp().pages.append,
                            args=(lambda x: p6.ui.pages.FinalUrlPage(x, title),),
                            )

    def extensionPoint(self, _context, for_):
        if self.__running:
            _context.action(discriminator=('Register', 'ExtensionPoint', for_),
                            callable=p6.api.getApp().pages.append,
                            args=(p6.extension.ExtensionPoint(for_), ),
                            )
    
    def storepage(self, _context):
        if self.__running:
            _context.action(discriminator=('RegisterPage', 'StorePage',
                                           p6.ui.pages.StorePage),
                            callable=p6.api.getApp().pages.append,
                            args=(p6.ui.pages.StorePage,),
                            )

    def fileselector(self, _context):
        if self.__running:
            _context.action(discriminator=('RegisterPage', 'FileSelector'),
                            callable=p6.api.getApp().pages.append,
                            args=(p6.ui.pages.FileSelectorPage,),
                            )

    def xmlpage(self, _context):
        if self.__running:
            _context.action(discriminator=('RegisterPage', 'XmlDisplayPage',
                                           p6.ui.pages.XmlMetadataPage),
                            callable=p6.api.getApp().pages.append,
                            args=(p6.ui.pages.XmlMetadataPage,),
                            )

    def xrcpage(self, _context, title, xrcfile, xrcid):
        if self.__running:
            _context.action(discriminator=('RegisterPage', xrcid,
                                           p6.ui.pages.XrcPage),
                            callable=p6.api.getApp().pages.append,
                            args=(p6.ui.pages.xrcpage(title, xrcfile, xrcid),),
                            )
        
    def page(self, _context, factory):
        if self.__running:
            _context.action(discriminator=('RegisterPage', factory),
                            callable=p6.api.getApp().pages.append,
                            args=(factory, )
                            )
    
class PreferencesDirective(object):
    """A preference set."""

    def __init__(self, _context, id, label, ):
        
        # initialize group settings
        self.id = id
        self.label = label

        self.__extobj = p6.app.extension.ExtensionPrefs(self.id, self.label)
        
        # add to the App's pref list once all the fields have been read
        _context.action(discriminator=('ExtensionPrefs', id),
                        callable=p6.api.getApp().prefs.__setitem__,
                        args=(self.id, self.__extobj, ),
                        )

    def field(self, _context, id, type, label=None):
        if label is None:
            label = id

        self.__extobj.fields[id] = p6.app.extension.ExtensionPrefField(id,
                                                                       type,
                                                                       label)
    
        
