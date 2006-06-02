import os
import wx

LOCALE = None

def initialize(root_dir, locale):
    """Initialize the wxPython internationalization machinery; if locale is 
    None, use the system default locale."""
    
    global LOCALE

    if locale is None:
        lang_id = wx.LANGUAGE_DEFAULT
    else:
        # look up the language info for the specified locale
        locale = wx.Locale.FindLanguageInfo(locale)
        if locale:
            # found the language; use it's identifier
            lang_id = locale.Language
        else:
            # unknown language; fall back to English
            lang_id = wx.LANGUAGE_ENGLISH
        
    LOCALE = wx.Locale(lang_id, wx.LOCALE_LOAD_DEFAULT)
    addCatalogPath(os.path.join(root_dir, 'locale'))

    # load the framework catalog
    loadCatalog('p6')

def addCatalogPath(pathname):
    global LOCALE

    LOCALE.AddCatalogLookupPathPrefix(pathname)

def loadCatalog(catalog_name):
    """Add a catalog to the lookup system."""

    global LOCALE

    LOCALE.AddCatalog(catalog_name)
    
def getLocale():
    """Return the application locale."""

    global LOCALE

    return LOCALE.GetCanonicalName()

