import zope.interface

class IWizardApp(zope.interface.Interface):
    groups = zope.interface.Attribute("Metadata groups.")
    appname = zope.interface.Attribute("")
    items = zope.interface.Attribute("Root level items.")
    
    
