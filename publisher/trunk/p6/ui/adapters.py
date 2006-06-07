import os.path

import wrappers

def fileItemDisplay(file_item):
    """Returns the "short name" for a file item, suitable for UI display."""

    return wrappers.LabelText(os.path.basename(file_item.getIdentifier()))
