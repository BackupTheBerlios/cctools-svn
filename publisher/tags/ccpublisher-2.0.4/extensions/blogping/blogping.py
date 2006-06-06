import p6
import wx

def AfterStored(event):
    """Subscriber for WorkStored (IStored) events -- prompts the user
    to publish to their blog.
    """

    result = wx.MessageDialog(
        None, "Blog this submission?", "Blogping", wx.YES_NO).ShowModal()

    if result == wx.ID_YES:
        # show the input dialog
        pass
        
        
