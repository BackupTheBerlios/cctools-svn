"""
pyarchive.cb_ftp

A wrapper for ftplib with basic callback facilities.

copyright 2004, Creative Commons, Nathan R. Yergler
"""

__id__ = "$Id$"
__version__ = "$Revision$"
__copyright__ = '(c) 2004, Creative Commons, Nathan R. Yergler'
__license__ = 'licensed under the GNU GPL2'

import ftplib

def noop(connection):
    pass

class FTP(ftplib.FTP):
    DEF_BLOCKSIZE=8192

    def storbinary(self, cmd, fp, blocksize=DEF_BLOCKSIZE, callback=noop):
        ''' Store a file in binary mode.'''
        if callback is None:
            callback = noop
            
        self.voidcmd('TYPE I')
        conn = self.transfercmd(cmd)
        while 1:
            buf = fp.read(blocksize)
            if not buf: break
            conn.send(buf)

            callback(conn)

        conn.close()
        return self.voidresp()

