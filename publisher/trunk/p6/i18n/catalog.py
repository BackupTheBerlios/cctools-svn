import os
import wx

LOCALE = None
PREFIXES = []

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
    global LOCALE, PREFIXES

    PREFIXES.append(pathname)
    LOCALE.AddCatalogLookupPathPrefix(pathname)

def __findCatalog(paths, catalog, lang):
    """Search for a catalog in paths, where paths is a sequence of possible
    locations.  Searches <n>/<lang>, then <n> for <catalog>.[m|p]o for each
    <n> in <paths>.  Returns the absolute path of the catalog.  If both
    .mo and .po are found, returns the most recently updated one.  If the
    catalog is not found, returns None."""
    
    for path in paths:
        mo_file = os.path.abspath(os.path.join(path, lang, catalog + ".mo"))
        po_file = os.path.abspath(os.path.join(path, lang, catalog + ".po"))
        
        po_exists = os.path.exists(po_file)
        mo_exists = os.path.exists(mo_file)

        if mo_exists and not(po_exists):
            return mo_file
        elif po_exists and not(mo_exists):
            return po_file
        elif po_exists and mo_exists:
            # both exist; check which is newer
            if os.path.getmtime(po_file) > os.path.getmtime(mo_file):
                return po_file
            else:
                return mo_file

    # catalog not found
    return None
            
def compileCatalog(catalog_path):
    """Compile the .po file specified by <catalog_path> to a binary gettext
    catalog.  The resulting binary catalog is placed in the same directory
    as the .po file."""

    import msgfmt

    # compile the catalog using msgfmt
    return msgfmt.make(catalog_path,
                       os.path.splitext(catalog_path)[0] + ".mo")
    
def loadCatalog(catalog_name):
    """Add a catalog to the lookup system."""

    global LOCALE, PREFIXES

    # check if this catalog needs to be recompiled
    catalog_path = __findCatalog(PREFIXES, catalog_name, getLocale())

    if catalog_path is not None:
        if os.path.splitext(catalog_path)[1] == '.po':
            # recompile the catalog
            compileCatalog(catalog_path)

    LOCALE.AddCatalog(catalog_name)
    
def getLocale():
    """Return the application locale."""

    global LOCALE

    return LOCALE.GetCanonicalName()

