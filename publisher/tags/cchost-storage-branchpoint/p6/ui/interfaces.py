"""
UI interfaces.
"""

import zope.interface

class ILabelText(zope.interface.Interface):
    """Wrapper interface for encapsultating label text."""

    text = zope.interface.Attribute("Text to be displayed in the label.")

class IEntryWidget(zope.interface.Interface):
    pass

class IPageList(zope.interface.Interface):

    def list():
        """Return the pages as a regular Python sequence."""
        
class IWizardPage(zope.interface.Interface):
    
    headline = zope.interface.Attribute("Text displayed at the top of the window.")
    xrcid = zope.interface.Attribute("A unique identifier for the page.")

    def validate(event):
        """Validate input for the page; return True if valid."""
      
    def onChanging(event):
        """Handler called before page is left."""
       
    def onChanged(event):
        """Handler called when page is displayed."""
