import zope.interface


class IEntryWidget(zope.interface.Interface):
    pass

class IWizardApp(zope.interface.Interface):
    groups = zope.interface.Attribute("Metadata groups.")
    appname = zope.interface.Attribute("")
    
class IWizardPage(zope.interface.Interface):
    
    headline = zope.interface.Attribute("Text displayed at the top of the window.")
    xrcid = zope.interface.Attribute("A unique identifier for the page.")

    def validate(self, event):
        """Validate input for the page; return True if valid."""
      
    def onChanging(self, event):
        """Handler called before page is left."""
       
    def onChanged(self, event):
        """Handler called when page is displayed."""
