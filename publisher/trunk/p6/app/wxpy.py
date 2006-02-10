import ConfigParser
import os

import wx
import wx.xrc

import zope.interface
import zope.component

import p6
import interfaces
import bananas

zope.configuration.xmlconfig.openInOrPlain = bananas.openInOrPlain

class WizApp(wx.App):
    zope.interface.implements(interfaces.IWizardApp)
    def __init__(self, appname=None, rsc_dir='.',
                 errlog=None, xrcfile=None,
                 frameclass=p6.ui.wizard.WizFrame,
                 confFile='app.zcml'):

        # initialize the metadata group list
        self.groups = []
        self.items = []

        # initialize the preferences container
        self.prefs = {}

        self.appname = appname
        self.resource_dir = rsc_dir
        self.errlog = errlog
        self.xrcfile = os.path.join(self.resource_dir, xrcfile)
        self.__frameclass = frameclass
        self.confFile = os.path.join(self.resource_dir, confFile)

        wx.App.__init__(self, filename=self.errlog)

    def OnInit(self):
        self.__configure()
        self.__loadPrefs()
        
        self.SetAppName(self.appname)

        wx.InitAllImageHandlers()

        self.__initUI()

        self.connectEvents()
        
        return True

    def OnExit(self):
        self.__savePrefs()

    def __loadPrefs(self):
        input = ConfigParser.ConfigParser()
        input.read((os.path.join(p6.api.getAppSupportDir(),
                                 'extprefs.conf'),))

        for section in input.sections():
            for key in input.options(section):
                try:
                    self.prefs[section].fields[key].value = \
                                                          input.get(section,
                                                                    key)
                except KeyError, e:
                    pass

    def __savePrefs(self):
        output = ConfigParser.ConfigParser()

        for prefset in self.prefs:
            output.add_section(prefset)

            for field in self.prefs[prefset].fields:
                output.set(prefset, field,
                           self.prefs[prefset].fields[field].value or '')


        output.write(file(os.path.join(p6.api.getAppSupportDir(),
                                       'extprefs.conf'), 'w'))
        
    def __configure(self):
        """Load the ZCML configuration for P6, the application and any
        extensions."""

        # load the core configuration
        self.context = zope.configuration.xmlconfig.file(self.confFile,
                                                         execute=False)

        # load extensions and plugins
        for epath in p6.app.extension.extPaths():
            for extconf in p6.app.extension.extConfs(epath):
                print extconf
                p6.app.extension.loadExtension(extconf, self.context)

        # perform the actions specified by the configuration files
        self.context.execute_actions()

        # expand any metadata page groups
        newpages = []
        for page in self.pages:
            if getattr(page, 'expand', False):
                newpages = newpages + [n for n in page(None)]
            else:
                newpages.append(page)

        self.pages = newpages
        del newpages

    def __makeMenu(self):
        """Generate the top-level menu bar and return the MenuBar object."""

        # load the basic menu bar
        res = wx.xrc.EmptyXmlResource()
        res.LoadFromString(self.MENU_XRC)
        menubar = res.LoadMenuBar('TOPMENU')

        # connect menu events
        self.Bind(wx.EVT_MENU,
                  lambda event: p6.ui.windows.prefs.P6PrefsWindow(self.GetTopWindow()).Show(),
                  id=wx.xrc.XRCID('MNU_PREFERENCES'))
        self.Bind(wx.EVT_MENU,
                  lambda event: self.GetTopWindow().Close(),
                  id=wx.xrc.XRCID('MNU_EXIT'))

        return menubar

    def __initUI(self):
        """Initialize any user interface elements -- in particular, the top
        level window and global menu bar."""

        self.main = self.__frameclass(self)
        self.main.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNFACE))
        self.main.Show(True)

        self.topmenu = self.__makeMenu()
        self.main.SetMenuBar(self.topmenu)
        # check if any extensions were loaded
        if len(self.prefs.keys()) == 0:
            # hide the preferences menu
            # XXX We currently hide the entire menu since it only has the prefs
            self.topmenu.EnableTop(1, False)
        
        
        self.SetTopWindow(self.main)
        self.main.SetSize(self.main.GetSize())
        
    def connectEvents(self):

        # listen for item addition events
        zope.component.provideHandler(
            zope.component.adapter(p6.storage.events.IItemSelected)(
                p6.api.deinstify(self.selectItem))
            )

        # create the root item
        self.items.append(p6.storage.items.RootItem())
        
    def selectItem(self, event):
        self.items.append(event.item)


    MENU_XRC = """
<resource>
  <object class="wxMenuBar" name="TOPMENU">
    <object class="wxMenu" name="MNU_FILE">
      <label>&amp;File</label>
      <object class="wxMenuItem" name="MNU_EXIT">
        <label>&amp;Exit</label>
      </object>
    </object>
    <object class="wxMenu" name="MNU_EDIT">
      <label>&amp;Edit</label>
      <object class="wxMenuItem" name="MNU_PREFERENCES">
        <label>&amp;Preferences</label>
      </object>
    </object>
  </object>
</resource>
"""
    
