"""p6.i18n

"""

import sys
import wx

# check if sys.setdefaultencoding still exists;
# if it does, we're probably running frozen

if getattr(sys, 'setdefaultencoding', False):
    sys.setdefaultencoding('utf-8')
    del sys.setdefaultencoding
    
from catalog import *

# use the wx i18n system
_ = wx.GetTranslation
