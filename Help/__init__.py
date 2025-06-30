import sys
import os
from typing import Dict
import webbrowser
import wx
import wx.html
from Icon import GetIcon

class HelpHTMLWindow(wx.html.HtmlWindow):
    def __init__(self, parent, filename, size = (800, 600)):
        wx.html.HtmlWindow.__init__(self, parent, size = size)

        base_path = getattr(sys, '_MEIPASS', '')
        if base_path:
            base_path = base_path + "/Help/"
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        self.LoadFile(f"{base_path}/{filename}")

        self.Bind(wx.html.EVT_HTML_LINK_CLICKED, self.HandleLinkClicked)

    # TODO - maybe check if we have "http(s)" at the start, and if not,
    # we're loading a local file and should use ourselves not the browser?
    def HandleLinkClicked(self, evt):
        linkinfo = evt.GetLinkInfo()
        page = linkinfo.GetHref()
        webbrowser.open(page)


class HelpWindow(wx.MiniFrame):
    def __init__(self, parent, filename):
        wx.MiniFrame.__init__(self, parent, title = filename, size = wx.Size(800, 600),
            style = wx.TINY_CAPTION|wx.DEFAULT_FRAME_STYLE)

        manualhtml = HelpHTMLWindow(self, filename)

        manualsizer = wx.BoxSizer(wx.VERTICAL)
        manualsizer.Add(manualhtml, 1, wx.EXPAND)

        self.SetSizer(manualsizer)

        self.Layout()

        HelpWindows[filename] = self

class HelpPopup(wx.PopupTransientWindow):
    def __init__(self, parent, filename):
        wx.PopupTransientWindow.__init__(self, parent)

        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(wx.Colour([127,127,127]))
        manualhtml = HelpHTMLWindow(self.panel, filename, size = (600, 100))

        manualsizer = wx.BoxSizer(wx.VERTICAL)
        manualsizer.Add(manualhtml, 1, wx.EXPAND|wx.ALL, 3)

        self.panel.SetSizer(manualsizer)

        # resize the whole thing to match manualhtml's correct vertical size
        virtsize = manualhtml.GetVirtualSize()
        virtsize.SetWidth(virtsize.GetWidth()+10)
        virtsize.SetHeight(virtsize.GetHeight()+10)
        self.SetSize(virtsize)
        self.panel.SetSize(virtsize)

        self.Layout()

        HelpPopups[filename] = self

class HelpButton(wx.BitmapButton):
    def __init__(self, parent, filename, type = "popup"):
        wx.BitmapButton.__init__(self, parent, -1, GetIcon('Help'))
        self.Filename = filename
        self.WinType = type

        self.Bind(wx.EVT_BUTTON, self.GetHelpHandler())

    def GetHelpHandler(self):
        if self.WinType == "popup":
            def OnClick(event): ShowHelpPopup(self, self.Filename, event)
        else:
            def OnClick(event): ShowHelpWindow(self, self.Filename, event)
        return OnClick


HelpWindows: Dict[str, HelpWindow] = {}
def ShowHelpWindow(parent, filename, _ = None):
    if not HelpWindows.get(filename, None):
        HelpWindows[filename] = HelpWindow(parent, filename)
    HelpWindows[filename].Show()

HelpPopups:  Dict[str, HelpPopup] = {}
def ShowHelpPopup(self, filename, event):
    if not HelpPopups.get(filename, None):
        HelpPopups[filename] = HelpPopup(self, filename)

    btn = event.GetEventObject()
    pos = btn.ClientToScreen( (0,0) )
    sz =  btn.GetSize()
    HelpPopups[filename].Position(pos, wx.Size(0, sz[1]))
    HelpPopups[filename].Popup()

