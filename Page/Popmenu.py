import wx
from Page import Page

from wx.lib.gizmos import TreeListCtrl

class Popmenu(Page):
    def __init__(self, parent):
        super().__init__(parent)

        Sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(Sizer)


