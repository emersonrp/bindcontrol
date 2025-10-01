import wx

import GameData
from Icon import GetIcon

import wx.lib.newevent
PowerSelectorChanged, EVT_POWERSELECTOR_CHANGED = wx.lib.newevent.NewCommandEvent()

class PowerSelector(wx.BitmapButton):
    def __init__(self, parent, page, pickername):
        super().__init__(parent, bitmap = GetIcon('UI', 'gear'))

        self.CtlName        = None
        self.CtlLabel       = None
        self.Page           = page
        self.Data           = None
        self.PickerName     = pickername
        self.DefaultToolTip = None
        self.Powers         = []

        self.Bind(wx.EVT_BUTTON, self.OnButtonClicked)
        page.Ctrls[pickername].Bind(wx.EVT_CHOICE, self.ClearPowers)

    def OnButtonClicked(self, _):
        # do not evt.Skip() here, we're going to throw a custom one instead
        menu = self.MakeMenu()
        self.PopupMenu(menu)

    def ClearPowers(self, evt = None):
        self.Powers = []
        if evt: evt.Skip()

    def AddPower(self, power: str):
        self.Powers.append(power)

    def GetValue(self):
        return self.Powers

    def SetValue(self, value):
        self.Powers = value

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
        wx.PostEvent(self, PowerSelectorChanged(wx.NewId(), control = self))
