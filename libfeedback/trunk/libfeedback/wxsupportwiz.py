#!/usr/bin/env python
"""
wxPython Technical Support Wizard (sort of).

Usage: wxsupportwiz.wxAddExceptHook('http://host.com/error.php')

- what happens if this is run when unconnected to the net?
- would be nice if the user could optionally enter some information about the problem, though of course I don't want it to get so complex that the user just cancels it

This sends the data using a CGI instead of by email because there's no guarantee that the user has setup an email account with MAPI.
Or I could always just bring up the user's web browser to a form already partially filled out.
The CGI could automatically match the error data to answers to already solved problems and suggest those.
So the whole wizard should probably be on the web.
For FAQs, could record how popular each answer is and then shown links to the top N answers.

can see XatXesizerDoc.cpp for a MAPI example. useful only for automatically including the user's email address
x automatically getting the user's email address seems hard, and what if there are multiple accounts, or none?

- sending the program's log would be nice to send too

The more work you postpone in your wxPython app until the wxWindows event loop has started, the more errors this will be able to catch.

If the cgi prints a line, this will assume it's a url and try to point the user's web browser to it. So you could, eg, popup help on the problem.

Having an exception occur in your exception handler is annoying.
"""

__author__ = 'Patrick Roberts'
__copyright__ = 'Copyright 2004 Patrick Roberts'
__license__ = 'Python'
__version__ = '1.0'

import os
import platform
import urllib
import urllib2
import sys
import time
import traceback
import urlparse
import webbrowser

import wx

import comm

def get_last_traceback(tb):
    while tb.tb_next:
        tb = tb.tb_next
    return tb


def format_namespace(d, indent=''):#    '):
    return '\n'.join(['%s%s: %s' % (indent, k, repr(v)[:10000]) for k, v in d.iteritems()])


ignored_exceptions = [] # a problem with a line in a module is only reported once per session

def wxAddExceptHook(postUrl, app_id, app_version='[No version]'):
    """
    wxMessageBox can't be called until the app's started
    - It would be nice if this used win32 directly, and didn't depend on wx being started, cuz that can't handle initial errors. Maybe have a temporary initial error handler that just uses a standard windows message dlg, then switch once wx is going.
    """
    
    def handle_exception(e_type, e_value, e_traceback):
        traceback.print_exception(e_type, e_value, e_traceback) # this is very helpful when there's an exception in the rest of this func
        last_tb = get_last_traceback(e_traceback)
        ex = (last_tb.tb_frame.f_code.co_filename, last_tb.tb_frame.f_lineno)
        if ex not in ignored_exceptions:
            ignored_exceptions.append(ex)

            err_msg = "%s has encountered an error. We apologize for\n"\
                      "the inconvenience.  You can help make this software\n"\
                      "better.\n\n"\
                      "Click OK to send an error report to Creative Commons.\n"\
                      "No personal information will be transmitted, only \n"\
                      "information about the state of the program when it \n"\
                      "crashed.\n\n" \
                      "If you choose to submit this crash report, you will\n"\
                      "receive a URL which you can use to track the status\n"\
                      "of your bug report." % (
                wx.GetApp().GetAppName())
            
            dlg = wx.MessageDialog(None, err_msg,
                               '%s: Unknown Error' % wx.GetApp().GetAppName(),
                               wx.OK|wx.CANCEL) 
            result = dlg.ShowModal()
            dlg.Destroy()
            
            if result == wx.ID_OK:
                # user authorizes crash report; try to import
                # p6.i18n to get the application locale
                try:
                    from p6.i18n import getLocale
                except ImportError, e:
                    getLocale = lambda : ''
                
                info = {
                    'app_id' : app_id,
                    'app_version' : app_version,
                    'platform' : platform.platform(),
                    'title' : '%s (%s)' % (e_type, e_value),
                    'message' : 'application locale: ' + getLocale()
                    }

                if e_traceback:
                    info['message'] = info['message'] + '\n\n' + ''.join(traceback.format_tb(e_traceback)) + '%s: %s' % (e_type, e_value)

                busy = wx.BusyCursor()
                bugUrl = comm.sendReport(postUrl, info)
                
                if bugUrl is not None:
                    result = wx.MessageDialog(None, "Your crash report has been sent.\n"
                          "You can track your report at\n"
                          "%s\n\nDo you want to open this page in your browser now?" % bugUrl,
                          caption="ccPublisher: Report Sent",
                          style=wx.YES|wx.NO).ShowModal()
                          
                    if result == wx.ID_YES:
                        # open the web browser
                        try:
                            webbrowser.open_new(bugUrl)
                        except WindowsError, e:
                            # some bizarre error occured opening the browser
                            wx.MessageDialog(None,
                                             "Unable to open browser; your "
                                             "crash report is available at %s"
                                             % bugURL,
                                             caption="ccPublisher: Error",
                                             style=wx.OK).ShowModal()
                else:
                    # XXX Show yet-another-error here 
                    # and humbly provide a way to submit a report manually
                    pass
                    
                del busy

	    sys.exit(1)


    sys.excepthook = lambda *args: wx.CallAfter(handle_exception, *args) # this callafter may be unnecessary since it looks like threads ignore sys.excepthook; could have all a thread's code be contained in a big try clause (possibly by subclassing Thread and replacing run())


if __name__ == '__main__':
    # need to be able to run this alone for testing
    pass
