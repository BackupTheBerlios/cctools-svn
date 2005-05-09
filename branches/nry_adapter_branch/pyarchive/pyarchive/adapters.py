import zope.component
import zope.interface

import p6

@zope.interface.implementer(p6.storage.interfaces.IInputStream)
@zope.component.adapter(interfaces.IArchiveFile)
def ArchiveFileInputStream(archive_file):
    return lambda:file(archive_file.filename, 'rb')

zope.component.provideAdapter(ArchiveFileInputStream)

