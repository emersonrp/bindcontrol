import wx
from Page import Page

from wx.lib.gizmos import TreeListCtrl

class PopmenuEditor(Page):
    def __init__(self, parent):
        super().__init__(parent)

        Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(Sizer)

        splitter = wx.SplitterWindow(self, style = wx.VERTICAL)
        splitter.SetMinimumPaneSize(150) # TODO do this less stupid

        MenuList = wx.ListBox(splitter, style = wx.LB_SINGLE)
        MenuList.Insert(['Test Item', 'Popmenu', 'Connor is good'], 0)

        MenuTree = Popmenu(splitter)

        splitter.SplitVertically(MenuList, MenuTree)

        ButtonPanel = wx.Panel(self)
        ButtonSizer = wx.BoxSizer(wx.VERTICAL)
        ButtonPanel.SetSizer(ButtonSizer)
        ButtonSizer.Add(wx.Button(ButtonPanel, label = "Write Popmenu"), 0, wx.EXPAND)
        ButtonSizer.Add(wx.Button(ButtonPanel, label = "Insert Item"), 0, wx.EXPAND)
        ButtonSizer.Add(wx.Button(ButtonPanel, label = "Insert Separator"), 0, wx.EXPAND)
        ButtonSizer.Add(wx.Button(ButtonPanel, label = "Insert Subment"), 0, wx.EXPAND)

        Sizer.Add(splitter, 1, wx.EXPAND)
        Sizer.Add(ButtonPanel, 0, wx.EXPAND)

        self.Layout()


class Popmenu(TreeListCtrl):
    def __init__(self, parent):
        super().__init__(parent)
