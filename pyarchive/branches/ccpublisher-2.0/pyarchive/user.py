"""User-related support functions for Internet Archive access."""

import ftplib

def validate(username, password):
    """Confirm that the username/password combination is valid; return True
    if valid, otherwise return False."""

    # attempt to open an FTP connection and log in
    try:
        server = ftplib.FTP('items-uploads.archive.org')
        server.login(username, password)

        # success; logout and return True
        server.quit()
        return True
    
    except ftplib.error_perm, e:
        # a login error occured
        pass
    
    return False
