
#!/usr/bin/env python3

# base class for all the individual tabs

import wx

import BindFile

class Page(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.Profile = parent
        self.TabTitle = type(self).__name__
        self.State = {}
        self.Profile.Pages[self.TabTitle] = self

    def help(self, event):

        if not (self.HelpWindow):
            HelpWindow = wx.MiniFrame .new( undef, -1, self.TabTitle + " Help",)
            BoxSizer   = wx.BoxSizer  .new( wx.VERTICAL )
            Panel      = wx.Panel     .new( HelpWindow, -1 )
            HelpText   = wx.StaticText.new( Panel, -1, self.HelpText, [10,10] )

            BoxSizer.Add( Panel, 1, wx.EXPAND )

            HelpWindow.SetSizer(BoxSizer)

            self.HelpWindow = HelpWindow

        self.HelpWindow.Show(not self.HelpWindow.IsShown())

    # stubs
    def InitKeys(self):
        profile = self.Profile

    def PopulateBindFiles():
        return
    def FillTab(self):
        return
    def HelpText():
        return 'Help not currently implemented here.'
