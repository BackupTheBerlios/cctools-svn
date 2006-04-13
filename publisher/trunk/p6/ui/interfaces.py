"""
UI interfaces.
"""

import zope.interface

class IEntryWidget(zope.interface.Interface):
    pass

class IPageList(zope.interface.Interface):

    def list():
        """Return the pages as a regular Python sequence."""
        
##     def size():
##         """Return the number of pages contained in this list."""

##     def get(index):
##         """Return the page at [index]."""
        
class IWizardPage(zope.interface.Interface):
    
    headline = zope.interface.Attribute("Text displayed at the top of the window.")
    xrcid = zope.interface.Attribute("A unique identifier for the page.")

    def validate(event):
        """Validate input for the page; return True if valid."""
      
    def onChanging(event):
        """Handler called before page is left."""
       
    def onChanged(event):
        """Handler called when page is displayed."""
