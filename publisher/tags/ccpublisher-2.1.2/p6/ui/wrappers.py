import zope.interface

import interfaces

class LabelText(object):
    zope.interface.implements(interfaces.ILabelText)

    def __init__(self, text):
        
        self.text = text
        
