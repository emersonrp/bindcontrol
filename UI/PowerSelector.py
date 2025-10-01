import wx
import wx.lib.stattext as ST
from typing import TYPE_CHECKING, Any

import GameData
from Icon import GetIcon
if TYPE_CHECKING: from Page import Page as bcPage

class PowerSelector(wx.BitmapButton):
    def __init__(self, parent, pickername):
        super().__init__(parent, bitmap = GetIcon('UI', 'copy'))

        self.CtlName        = None
        self.CtlLabel       = None
        self.Page           = None
        self.Data           = None
        self.PickerName     = pickername
        self.DefaultToolTip = None
        self.Powers         = []

        self.Bind(wx.EVT_BUTTON, self.OnButtonClicked)

    def OnButtonClicked(self, _):
        # do not skip event here, we're going to throw a custom one instead
        menu = self.MakeMenu()
        self.PopupMenu(menu)

    ### TODO TODO TODO need to clean out self.Powers if the picker changes.

    def MakeMenu(self):
        profile = wx.App.Get().Main.Profile
        popupMenu = wx.Menu()
        pickername = self.PickerName
        picker = None
        powerset = ''
        if self.Page:
            picker = self.Page.Ctrls[pickername]
            powerset = picker.GetStringSelection()

        if pickername in ('Primary', 'Secondary', 'Epic'):
            powers = GameData.Archetypes[profile.Archetype()][pickername][powerset]
        else:
            powers = GameData.PoolPowers[powerset]

        for power in powers:
            item = popupMenu.AppendCheckItem(wx.ID_ANY, power)
            if power in self.Powers:
                item.Check(True)

        popupMenu.Bind(wx.EVT_MENU, self.OnMenuClicked)

        return popupMenu

    def OnMenuClicked(self, evt):
        popupmenu = evt.GetEventObject()
        items = popupmenu.GetMenuItems()

        powers = [item.GetItemLabel() for item in items if item.IsChecked()]
        self.Powers = powers
