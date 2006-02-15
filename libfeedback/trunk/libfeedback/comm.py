import urllib
import urllib2

def sendReport(postUrl, fields):
    """Posts a crash or bug report to a specified URL and returns the response."""
    
    try:
        f = urllib2.urlopen(postUrl, data=urllib.urlencode(fields))
        bugUrl = f.read().strip()
        
        return bugUrl
    
    except IOError:
        # if we had an error, return None
        pass
    
    return None
