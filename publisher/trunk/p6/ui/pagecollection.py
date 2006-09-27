__id__ = "$Id$"
__version__ = "$Revision$"
__copyright__ = '(c) 2004, Creative Commons, Nathan R. Yergler'
__license__ = 'licensed under the GNU GPL2'

from UserList import UserList

import zope.interface
import p6.extension.point
from p6.i18n import _

import os.path

class IPageCollection(zope.interface.Interface):
   pass

class PageCollection(UserList):
   """A collection of pages which contains support for extension points."""
   def __init__(self, pages=[]):
      UserList.__init__(self, pages)
      
      self.page_stack = []
      self.__cur_index = 0

   def current(self):
      """Returns the current page."""
      return self.data[self.__cur_index]

   def __checkPage(self):
      """Checks the current page to see if it's an extension point.
      If it is, it attempts to expand it into a sequence of pages and
      makes it active."""
      
      # check if the current page is an extension point
      if (isinstance(self.data[self.__cur_index],
                     p6.extension.point.ExtensionPoint)):
         # this is an extension point
         ext_point = self.data[self.__cur_index]

         # see if anyone implements this extension point
         implementors = ext_point.implementors()

         if implementors:
            # someone does, push the current page state and use the new one
            self.page_stack.append( (self.data, self.__cur_index) )

            # get a handle to the parent object for realized pages
            page_parent = p6.api.getApp().GetTopWindow().getPageParent()

            # construct the pages
            realized_pages = []

            for implementor in implementors:
               for p in implementor:
                  realized_pages.append(p(page_parent))

            self.data = realized_pages
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
      while (self.__cur_index >= len(self.data)) or \
                not(self.__checkPage()):


         if self.__cur_index >= len(self.data):
            # pop off the top item in the stack
            self.data, self.__cur_index = self.page_stack[-1]
            del self.page_stack[-1]

         # increment our old current index
         self.__cur_index = self.__cur_index + 1

      # return the new current page
      return self.current()

   def previous(self):
      self.__cur_index = self.__cur_index - 1

      # see if we're at the top of the list
      while (self.__cur_index < 0):
         # pop off the top item in the stack
         self.data, self.__cur_index = self.page_stack[-1]
         del self.page_stack[-1]

         # check if we're on an extension point
         # (we are by definition if we just had to pop something off the stack)
         while isinstance(self.data[self.__cur_index],
                          p6.extension.point.ExtensionPoint):
            self.__cur_index = self.__cur_index - 1

      # return the new current page
      return self.current()
   
   def is_first(self):

      # XXX this doesn't work if the first page is actually an extension point
      return (self.__cur_index == 0 and len(self.page_stack) == 0)

   def is_last(self):

      if self.__cur_index < len(self.data) - 1:
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
