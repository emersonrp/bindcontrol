#!/usr/bin/python

import wx

class Main(wx.Frame):
    def __init__(self):
        super().__init__(None)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(sizer)

        self.Display = wx.StaticText(self)
        sizer.Add(self.Display, 1, wx.ALIGN_CENTER)
        self.Match = wx.StaticText(self, label = 'This text should match window')
        sizer.Add(self.Match, 1, wx.ALIGN_CENTER)

        self.Bind(wx.EVT_SYS_COLOUR_CHANGED, self.OnSysColourChanged)

        self.OnSysColourChanged()

    def OnSysColourChanged(self, evt = None):
        if evt: evt.Skip()
        handlermode = 'Dark' if wx.SystemSettings.GetAppearance().IsDark() else 'Light'
        bgcolour    = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
        textcolour  = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)

        self.Display.SetLabel(f"New Mode is {handlermode}")

        self.Match.SetBackgroundColour(bgcolour)
        self.Match.SetForegroundColour(textcolour)

        self.Refresh()
        self.Layout()

app = wx.App(False)
frame = Main()
frame.Show()
app.MainLoop()
