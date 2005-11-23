import zope.interface
import zope.component

class IEmbeddable(zope.interface.Interface):
    """An interface to an object which supports license embedding."""
    item = zope.interface.Attribute("The item which will be embedded.")
    
    def embed(license, v_url, year, holder):
        """Embed the specified license in the wrapped item."""
        
