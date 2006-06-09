__id__ = "$Id$"
__version__ = "$Revision$"
__copyright__ = '(c) 2004, Creative Commons, Nathan R. Yergler'
__license__ = 'licensed under the GNU GPL2'

import wx
import wx.xrc
from wx.xrc import XRCCTRL

import xrc as ccwx_xrc

import p6.extension.point
import os.path

import ccwx.stext
ccEVT_XRCWIZ_PAGE_CHANGING = wx.NewEventType()
ccEVT_XRCWIZ_PAGE_CHANGED  = wx.NewEventType()

EVT_XRCWIZ_PAGE_CHANGING = wx.PyEventBinder(ccEVT_XRCWIZ_PAGE_CHANGING, 1)
EVT_XRCWIZ_PAGE_CHANGED  = wx.PyEventBinder(ccEVT_XRCWIZ_PAGE_CHANGED,  1)

class PageCollection(object):
   """A collection of pages which contains support for extension points."""
   def __init__(self, pages=[]):
      self.pages = pages
      self.page_stack = []
      self.__cur_index = 0

   def current(self):
      """Returns the current page."""
      return self.pages[self.__cur_index]

   def __checkPage(self):
      """Checks the current page to see if it's an extension point.
      If it is, it attempts to expand it into a sequence of pages and
      makes it active."""
      
      # check if the current page is an extension point
      if (isinstance(self.pages[self.__cur_index],
                     p6.extension.point.ExtensionPoint)):
         # this is an extension point
         ext_point = self.pages[self.__cur_index]

         # see if anyone implements this extension point
         implementors = ext_point.implementors()

         if implementors:
            # someone does, push the current page state and use the new one
            self.page_stack.append( (self.pages, self.__cur_index) )

            # get a handle to the parent object for realized pages
            page_parent = p6.api.getApp().GetTopWindow().getPageParent()

            # construct the pages
            realized_pages = []

            for implementor in implementors:
               for p in implementor:
                  realized_pages.append(p(page_parent))

            self.pages = realized_pages
            self.__cur_index = 0

            # the extension point existed and was successfully expanded
            return True
         else:

            # the e.p. existed, but is not implemented by anyone
            return False

      # no extension point
      return True

   def next(self):

      self.__cur_index = self.__cur_index + 1
      
      # see if we're at the end of this list or at a non-expanding e.p.
      while (self.__cur_index >= len(self.pages)) or \
                not(self.__checkPage()):


         if self.__cur_index >= len(self.pages):
            # pop off the top item in the stack
            self.pages, self.__cur_index = self.page_stack[-1]
            del self.page_stack[-1]

         # increment our old current index
         self.__cur_index = self.__cur_index + 1

   def previous(self):
      self.__cur_index = self.__cur_index - 1

      # see if we're at the top of the list
      while (self.__cur_index < 0):
         # pop off the top item in the stack
         self.pages, self.__cur_index = self.page_stack[-1]
         del self.page_stack[-1]

         # check if we're on an extension point
         # (we are by definition if we just had to pop something off the stack)
         while isinstance(self.pages[self.__cur_index],
                          p6.extension.point.ExtensionPoint):
            self.__cur_index = self.__cur_index - 1


   def is_first(self):

      # XXX this doesn't work if the first page is actually an extension point
      return (self.__cur_index == 0 and len(self.page_stack) == 0)

   def is_last(self):

      if self.__cur_index < len(self.pages) - 1:
         # we have *at least* one more page
         return False

      # check each other item in the stack
      for i in range(len(self.page_stack) - 1, -1, -1):
         page_list, index = self.page_stack[i]
         if index < len(page_list) - 1:
            
            # items exist in this set of pages; see if they're
            # pages or e.p's; if e.p's, make sure they have implementors
            for j in range(index + 1, len(page_list)):
               if isinstance(page_list[j], p6.extension.point.ExtensionPoint):

                  if not(page_list[j].implementors()):
                     # not one implements this extension point
                     continue
                  else:
                     # we assume *someone* implements it... not
                     # necessarily safe, but a compromise...
                     return False

               else:
                  # at least one real page remains
                  return False
               
            # return False

      return True

   def __len__(self):
      return len(self.pages)
   
class XrcWizardEvent(wx.PyCommandEvent):
   def __init__(self, evt_id, win_id, direction=True, page=None):
      wx.PyCommandEvent.__init__(self, evt_id, win_id)

      self.page = page
      self.direction = direction

      self.__allowed = True

   def GetPage(self):
      return self.page

   def Veto(self):
      self.__allowed = self.__allowed and False

   def Allow(self):
      self.__allowed = self.__allowed and True

   def IsAllowed(self):
      return self.__allowed

class XrcWiz(wx.Frame):
   def __init__(self, parent, filename='', id=None):
      self.app = parent
      self.xrcid = id

      self.pages = PageCollection()
      # self.cur_page = -1

      # create a handle to the XML resource file
      self.xrc = wx.xrc.EmptyXmlResource()
      self.xrc.InsertHandler(ccwx.stext.StaticWrapTextXmlHandler())
      self.xrc.Load(filename)
      
      # create the frame's skeleton
      pre = wx.PreFrame()

      # load the actual definition from the XRC
      self.xrc.LoadOnFrame(pre, None, id)

      # finish creation
      self.PostCreate(pre)
      self.SetMinSize((488,450))
      self.SetAutoLayout(True)

      self.Bind(wx.EVT_BUTTON, self.onNext, XRCCTRL(self, "CMD_NEXT"))
      self.Bind(wx.EVT_BUTTON, self.onPrev, XRCCTRL(self, "CMD_PREV"))

      self.Bind(EVT_XRCWIZ_PAGE_CHANGED,  self.OnPageChanged)
      self.Bind(EVT_XRCWIZ_PAGE_CHANGING, self.OnPageChanging)

   def setPageCollection(self, new_collection):
      self.pages = new_collection
      
   def __detachCurrent(self, event=None):
      """Detach and hide the current page."""
      
      XRCCTRL(self, "PNL_BODY").GetSizer().Hide(self.pages.current())
      XRCCTRL(self, "PNL_BODY").GetSizer().Detach(self.pages.current())

   def __addCurrent(self, event=None):

       # add and show the new page
       XRCCTRL(self, "PNL_BODY").GetSizer().Insert(0,
                                                   self.pages.current(),
                                                   flag=wx.EXPAND)

       self.pages.current().Show()
       self.pages.current().Layout()

       # update the headline
       XRCCTRL(self, "LBL_HEADER_TEXT").SetLabel(
          self.pages.current().headline)
       
       self.__updateNavBtns(event)
       self.Layout()

   addCurrent = __addCurrent

   def __updateNavBtns(self, event=None):

      if self.pages.is_last():
         XRCCTRL(self, "CMD_NEXT").SetLabel('Quit')
      else:
         XRCCTRL(self, "CMD_NEXT").SetLabel('Next')

      if self.pages.is_first():
         XRCCTRL(self, "CMD_PREV").Disable()
      else:
         XRCCTRL(self, "CMD_PREV").Enable()

      XRCCTRL(self, "CMD_NEXT").Enable()
       
   def onCancel(self, event):
      self.Close()

   def updateLayout(self):
      """Sets the current page to the specified XRCID."""

      # refresh the window
      self.GetSizer().Layout()      
      self.Refresh()

   def onNext(self, event):
       change_event = XrcWizardEvent(ccEVT_XRCWIZ_PAGE_CHANGING,
                                     self.pages.current().GetId(), 
                                     direction=True, 
                                     page=self.pages.current())
       self.GetEventHandler().ProcessEvent(change_event)

       if not change_event.IsAllowed():
          return False

       # check for Finish instead of next
       if (self.pages.is_last()):
          # either at the end of the list of pages, or we've hit a None 
          # (which flags for stop)
          self.Close()
          return

       self.__detachCurrent()
       self.pages.next()
       self.__addCurrent()
       
       self.updateLayout()
       
       change_event = XrcWizardEvent(ccEVT_XRCWIZ_PAGE_CHANGED,
                                     self.pages.current().GetId(), 
                                     direction=True, 
                                     page=self.pages.current())
       self.GetEventHandler().ProcessEvent(change_event)

       XRCCTRL(self, "PNL_BODY").Layout()
       self.Layout()

   def onPrev(self, event):
       change_event = XrcWizardEvent(ccEVT_XRCWIZ_PAGE_CHANGING,
                                     self.pages.current().GetId(), 
                                     direction=False, 
                                     page=self.pages.current())
       self.GetEventHandler().ProcessEvent(change_event)

       if not change_event.IsAllowed():
          return False


       self.__detachCurrent()
       self.pages.previous()
       self.__addCurrent()
       
       self.updateLayout()

       change_event = XrcWizardEvent(ccEVT_XRCWIZ_PAGE_CHANGED,
                                     self.pages.current().GetId(), 
                                     direction=False, 
                                     page=self.pages.current())
       self.GetEventHandler().ProcessEvent(change_event)

   def getPageParent(self):
     """Return the object which should serve as parent for page objects.

     @rtype: L{wx.Window}
     """
     return wx.xrc.XRCCTRL(self, "PNL_BODY")

   def OnPageChanged(self, event):
      if hasattr(event.GetPage(), 'onChanged'):
         event.GetPage().onChanged(event)

      wx.GetApp().GetTopWindow().SendSizeEvent()
      

   def OnPageChanging(self, event):
       if not event.GetPage().validate(event):
           event.Veto()

       if hasattr(event.GetPage(), 'onChanging'):
          event.GetPage().onChanging(event)

class XrcWizPage(wx.PyPanel):
   def __init__(self, parent, xrc, xrcid, headline='__change_me__'):
      self.xrcid = xrcid
      self.parent = parent
      
      self.headline = headline
      
      # create the frame's skeleton
      pre = wx.PrePyPanel()

      # load the actual definition from the XRC
      # check if we were passed a filename, XRC fragment or XmlResource
      if isinstance(xrc, (str, unicode)):
         if os.path.exists(xrc):
            # the string is a filename
            res = ccwx_xrc.load(xrc) 
         else:
            # the string is an XRC fragment
            res = ccwx_xrc.resource()
            res.LoadFromString(xrc)
      elif isinstance(xrc, wx.xrc.XmlResource):
         res = xrc
         
      res.LoadOnPanel(pre, XRCCTRL(parent, "PNL_BODY"), xrcid)

      # finish creation
      self.PostCreate(pre)
      self.SetAutoLayout(True)
      
      self.Fit()
      self.Hide()
      
   def validate(self, event):
      return True
      
   def onChanging(self, event):
       pass
       
   def onChanged(self, event):
       pass
       
  
