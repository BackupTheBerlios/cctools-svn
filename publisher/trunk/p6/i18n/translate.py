import wx

I18N_FILE = None

def dump_ (str_arg):
    """Dump strings for translation to a text file."""
    global I18N_FILE
    
    if I18N_FILE is None:
        I18N_FILE = file('strings.txt', 'w')
        
    I18N_FILE.write(str_arg)
    I18N_FILE.write('\n')

    return str_arg

