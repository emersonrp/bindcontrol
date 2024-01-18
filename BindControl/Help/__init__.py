import sys
import os
from typing import Dict
import wx
import wx.html
from Icon import GetIcon

class HelpWindow(wx.MiniFrame):
    def __init__(self, parent, filename):
        wx.MiniFrame.__init__(self, parent, size = (800, 600),
                              style = wx.CAPTION|wx.CLOSE_BOX|wx.STAY_ON_TOP|wx.RESIZE_BORDER)

        self.manualsizer = wx.BoxSizer(wx.VERTICAL)
        self.manualpane  = wx.html.HtmlWindow(self, size = (800, 600))
        self.manualpane.SetRelatedFrame(self, '%s')
        self.manualsizer.Add(self.manualpane, 1, wx.EXPAND)
        self.SetSizer(self.manualsizer)
        base_path = getattr(sys, '_MEIPASS', '')
        if base_path:
            base_path = base_path + "/Help/"
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        self.manualpane.LoadFile(f"{base_path}/{filename}")
        self.Layout()

        HelpWindows[filename] = self

class HelpButton(wx.BitmapButton):
    def __init__(self, parent, filename):
        wx.BitmapButton.__init__(self, parent, -1, GetIcon('Help'))
        self.Filename = filename

        self.Bind(wx.EVT_BUTTON, self.GetHelpHandler())

    def GetHelpHandler(self):
        def OnClick(_): ShowHelpWindow(self.Parent, self.Filename)
        return OnClick

HelpWindows: Dict[str, HelpWindow] = {}
def ShowHelpWindow(parent, filename):
    if not HelpWindows.get(filename, None):
        HelpWindows[filename] = HelpWindow(parent, filename)
    HelpWindows[filename].Show()

