import exceptions
import webbrowser as stdlib_wb
import platform

def open(url, new=0, autoraise=1):
    """Proxy call to stdlib webbrowser.open which catches platform-specific
    exceptions.  Returns True if the webbrowser.open call succeeds; returns
    False if an exception is thrown."""

    PLATFORM = platform.system().lower()

    try:
        if (PLATFORM == "windows"):
            try:
                stdlib_wb.open(url, new, autoraise)
            except exceptions.WindowsError, e:
                return False

        elif (PLATFORM == "darwin"):
            import MacOS

            try:
                stdlib_wb.open(url, new, autoraise)
            except MacOS.Error, e:
                return False

        else:
            stdlib_wb.open(url, new, autoraise)
            
    except stdlib_wb.Error, e:
        return False

    return True

def open_new(url):
    return open(url, True)
