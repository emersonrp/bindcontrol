import wx
from Page import Page

from wx.lib.gizmos import TreeListCtrl

class PopmenuEditor(Page):
    def __init__(self, parent):
        super().__init__(parent)

        Sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(Sizer)

        splitter = wx.SplitterWindow(self, style = wx.VERTICAL)

        MenuList = wx.ListBox(splitter, style = wx.LB_SINGLE)
        MenuList.Insert(['Test Item', 'Popmenu', 'Connor is good'], 0)

        MenuTree = TreeListCtrl(splitter)

        splitter.SplitVertically(MenuList, MenuTree)

        ButtonPanel = wx.Panel(self)

        Sizer.Add(splitter, 1, wx.EXPAND)
        Sizer.Add(ButtonPanel, 0, wx.EXPAND)

        self.Layout()
