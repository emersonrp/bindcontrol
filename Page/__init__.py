
#!/usr/bin/env python3

# base class for all the individual tabs

import wx

import BindFile

class Page(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.Profile = parent
        self.TabTitle = type(self).__name__

        self.Controls = {}


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
    def PopulateBindFiles(self):
        return
    def FillTab(self):
        return
    def HelpText(self):
        return 'Help not currently implemented here.'

    def GetState(self, key):
        control = self.Controls[key]

        # return control.Value()  # except the right thing for different control types

    def SetState(self, key, value):
        control = self.Controls[key]

        # control(key).SetValue(value) # except the right thing for all types
