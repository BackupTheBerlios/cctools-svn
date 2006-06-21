"""p6.i18n

"""
import sys

# check if sys.setdefaultencoding still exists; if it does, we're probably running frozen
if getattr(sys, 'setdefaultencoding', False):
    sys.setdefaultencoding('utf-8')
    del sys.setdefaultencoding
    
from catalog import *
from translate import *

# Uncomment the following line for development mode -- extract strings
#_ = dump_

# Uncomment the following line for production -- translate strings
_ = wx.GetTranslation
