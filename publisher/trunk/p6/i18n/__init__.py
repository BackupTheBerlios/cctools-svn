import os
import wx

I18N_FILE = None
LOCALE = None

def initialize(root_dir):
    """Initialize the wxPython internationalization machinery."""
    global LOCALE
    
    LOCALE = wx.Locale(wx.LANGUAGE_DEFAULT, wx.LOCALE_LOAD_DEFAULT)
    LOCALE.AddCatalogLookupPathPrefix(os.path.join(root_dir, 'locale'))

    # load the framework catalog
    loadCatalog('p6')

def loadCatalog(catalog_name):
    """Add a catalog to the lookup system."""

    global LOCALE

    LOCALE.AddCatalog(catalog_name)
    
def getLocale():
    """Return the application locale."""

    global LOCALE

    return LOCALE.GetCanonicalName()

def dump_ (str_arg):
    """Dump strings for translation to a text file."""
    global I18N_FILE
    
    if I18N_FILE is None:
        I18N_FILE = file('strings.txt', 'w')
        
    I18N_FILE.write(str_arg)
    I18N_FILE.write('\n')

    print str_arg
    return str_arg


# Uncomment the following line for development mode -- extract strings
#_ = dump_

# Uncomment the following line for production -- translate strings
_ = wx.GetTranslation
