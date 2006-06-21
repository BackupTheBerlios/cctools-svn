"""
Adapters for storage subsystem
"""

def fileItemMetadataProvider(fileItem):
    """Adapter from L{p6.storage.interfaces.IFileItem} to
    L{p6.metadata.interfaces.IMetadataProvider}; IFileItem actually
    indirectly provides IMetadataProvider so this just explicitly
    states that.
    """
    
    # Just return the passed in fileItem since it indirectly provides
    # the desired interface.
    
    return fileItem
