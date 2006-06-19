"""\
Components with word wrap magic.
"""

import wx
from wx.lib.stattext import GenStaticText

class WordWrapTextXmlHandler(wx.xrc.XmlResourceHandler):
    def __init__(self):
        wx.xrc.XmlResourceHandler.__init__(self)
        
        # Specify the styles recognized by objects of this type
        self.AddStyle("wx.NO_3D", wx.NO_3D)
        self.AddStyle("wx.TAB_TRAVERSAL", wx.TAB_TRAVERSAL);
        self.AddStyle("wx.WS_EX_VALIDATE_RECURSIVELY",
                      wx.WS_EX_VALIDATE_RECURSIVELY);
        self.AddStyle("wx.CLIP_CHILDREN", wx.CLIP_CHILDREN);

        self.AddWindowStyles()

    def CanHandle(self, node):
        return self.IsOfClass(node, "wxStaticText")

    def DoCreateResource(self):
        # we only currently support creation from scratch
        assert self.GetInstance() is None
 
        # create the new instance and return it
        swt = WordWrapText(self.GetParentAsWindow(),
                              self.GetID(),
                              self.GetText('label'),
                              self.GetPosition(),
                              self.GetSize(),
                              self.GetStyle("style", wx.TAB_TRAVERSAL),
                              self.GetName(),
                              )
        return swt


class WordWrapIterator:
    'Mixin to iterate on words'

    def wrappedlines(self, x, y, width, height, label, dc=None):
        'Iterate on printed lines'
        # height is ignored.
        if dc is None:
            dc = self
        words = []
        lines = label.split('\n')
        j = 0
        while 1:
            if not words:                                       # empty words: get next line
                if j == len(lines):                             # out of lines, done
                    break                                       # we are done
                words.extend(lines[j].split())                  # get next line
                j += 1
            w, i, space = 0, 0, ' '
            while i < len(words):
                ww, h = dc.GetTextExtent(words[i] + space)      # add space!
                space = ' '                                     # for non-first word in line: add space
                if w + ww > width:
                    break
                w, i = ww + w, i + 1
            if i == 0:
                if len(words):                                  # if not an empty line,
                    i = 1                                       # put at least one word in a line
                else:                                           # Else it will be an empty line.
                    w, h = dc.GetTextExtent('W')                # empty lines have height too
            line = ' '.join(words[:i])                          # line that gets printed
            words = words[i:]                                   # words to carry over to next line
            y += h
            yield x, y - h, w, h, line

class WordWrapText(GenStaticText, WordWrapIterator):
    'Generic static text with word wrap capability'

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        #dc = wxPaintDC(self)
        width, height = self.GetClientSize()
        if not width or not height:
            return

        clr = self.GetBackgroundColour()
        backBrush = wx.Brush(clr, wx.SOLID)
        if wx.Platform == "__WXMAC__": # and clr == self.defBackClr:
            # if colour still the default the use the striped background on Mac
            backBrush.MacSetTheme(1) # 1 == kThemeBrushDialogBackgroundActive
        dc.SetBackground(backBrush)

        dc.SetTextForeground(self.GetForegroundColour())
        dc.Clear()
        dc.SetFont(self.GetFont())
        label = self.GetLabel()
        style = self.GetWindowStyleFlag()

        for x, y, w, h, line in self.wrappedlines(0, 0, width, height, label):
            # get alignment
            if style & wx.ALIGN_RIGHT:
                x = width - w
            if style & wx.ALIGN_CENTER:
                x = (width - w)/2
            # print out
            dc.DrawText(line, x, y)

    def DoGetBestSize(self):
        """Overridden base class virtual.  Determines the best size of the
        button based on the label size."""
        label = self.GetLabel()
        totalHeight, maxWidth = 0, 0
        width, height = self.GetClientSize()                    # original size (height is not important)

        for x, y, w, h, line in self.wrappedlines(0, 0, width, height, label):
            totalHeight += h
            maxWidth = max(maxWidth, w)

        # width is kept, height is stretched.
        return wx.Size(maxWidth, totalHeight)

# -------------------------------------------------------------

if __name__ == "__main__":

    class Test(wx.App):
        def OnInit(self):

            # ---
            # Make our main frame and start it
            frame = wx.Frame(None, -1, "")
            sizer = wx.BoxSizer(wx.VERTICAL)
            wrap = WordWrapText(frame, -1, '''XX XX XX
A very very long, very, very, very very long line, that is very long indeed, I say, long, long, long.
A not so long line but long enough to wrap over.
A short line to finish.''', size=(60, -1))
            #wrap.SetLabel('A small txt')
            sizer.Add(wrap, 1, wx.EXPAND)
            frame.SetSizerAndFit(sizer)
            frame.SetAutoLayout(1)
            frame.Show(1)
            self.SetTopWindow(frame)
            return 1

    test = Test()
    test.MainLoop()
