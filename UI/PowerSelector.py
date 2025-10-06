import wx
import wx.lib.stattext as ST
from typing import Any

import GameData
from Icon import GetIcon

import wx.lib.newevent
PowerSelectorChanged, EVT_POWERSELECTOR_CHANGED = wx.lib.newevent.NewCommandEvent()

class PowerSelector(wx.BitmapButton):
    def __init__(self, parent, page, pickername):
        super().__init__(parent, bitmap = GetIcon('UI', 'select'))

        self.CtlLabel : ST.GenStaticText | wx.StaticText | None = None
        self.Page                                               = page
        self.Data     : Any                                     = None
        self.CtlName                                            = ''
        self.PickerName                                         = pickername
        self.DefaultToolTip                                     = ''
        self.Powers                                             = []

        self.Bind(wx.EVT_BUTTON, self.OnButtonClicked)
        page.Ctrls[pickername].Bind(wx.EVT_CHOICE, self.ClearPowers)

    def OnButtonClicked(self, _):
        # do not evt.Skip() here, we're going to throw a custom one instead when the popup closes
        powerlist = Popup(self.Page, self)
        evtpos = wx.GetMousePosition()
        powerlist.Position(wx.Point(evtpos.x + 5, evtpos.y + 5), wx.DefaultSize)
        powerlist.Popup()

    def ClearPowers(self, evt = None):
        self.Powers = []
        wx.PostEvent(self, PowerSelectorChanged(wx.NewId(), control = self))
        if evt: evt.Skip()

    def AddPower(self, power: str):
        self.Powers.append(power)

    def GetValue(self):
        return self.Powers

    def SetValue(self, value):
        self.Powers = value

class Popup(wx.PopupTransientWindow):
    def __init__(self, parent, powerselector: PowerSelector):
        super().__init__(parent)

        self.PowerSelector = powerselector

        panel = wx.Panel(self)
        popup = wx.CheckListBox(panel, style = wx.LB_SINGLE)

        manualsizer = wx.BoxSizer(wx.VERTICAL)
        manualsizer.Add(popup, 1, wx.EXPAND|wx.ALL, 3)

        panel.SetSizer(manualsizer)

        pickername = self.PowerSelector.PickerName

        powerset = ''
        picker = parent.Ctrls[pickername]
        powerset = picker.GetStringSelection()

        if pickername in ('Primary', 'Secondary', 'Epic'):
            powers = GameData.Archetypes[parent.Profile.Archetype()][pickername][powerset]
        else:
            powers = GameData.PoolPowers[powerset]

        popup.InsertItems(powers,0)
        for i,power in enumerate(powers):
            if power in self.PowerSelector.Powers:
                popup.Check(i)

        popup.Bind(wx.EVT_LEFT_DOWN, self.OnPopupClicked)

        panel.Fit()
        panel.Layout()
        self.Fit()
        self.Layout()

    def OnPopupClicked(self, evt):
        popup = evt.GetEventObject()
        popup.SetSelection(wx.NOT_FOUND)

        # If we are first popping up the menu, don't toggle the first element.
        # This is ugly and annoying.
        clpoint = popup.ScreenToClient(wx.GetMousePosition())
        if (sel := popup.HitTest(clpoint)) == wx.NOT_FOUND:
            return

        popup.Check(sel, not popup.IsChecked(sel))

        powers = [popup.GetString(i) for i in popup.GetCheckedItems()]
        self.PowerSelector.Powers = powers

    def OnDismiss(self):
        wx.PostEvent(self.PowerSelector.Page, PowerSelectorChanged(wx.NewId(), control = self.PowerSelector))
        self.DestroyLater()
