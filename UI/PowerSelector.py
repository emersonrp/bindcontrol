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
        powerlist.CheckList.SetSelection(wx.NOT_FOUND)

    def ClearPowers(self, evt = None):
        if evt: evt.Skip()
        self.Powers = []
        wx.PostEvent(self.Page, PowerSelectorChanged(wx.NewId(), control = self))

    def GetValue(self):
        return self.Powers

    def SetValue(self, value):
        self.Powers = value

class Popup(wx.PopupTransientWindow):
    def __init__(self, parent, powerselector: PowerSelector):
        super().__init__(parent)

        self.PowerSelector = powerselector

        pickername = self.PowerSelector.PickerName
        powerset = parent.Ctrls[pickername].GetStringSelection()

        if pickername in ('Primary', 'Secondary', 'Epic'):
            powers = GameData.Archetypes[parent.Profile.Archetype()][pickername][powerset]
        else:
            powers = GameData.PoolPowers[powerset]

        self.CheckList = wx.CheckListBox(self, choices = powers, style = wx.LB_SINGLE)
        for i,power in enumerate(powers):
            if power in self.PowerSelector.Powers:
                self.CheckList.Check(i)
        self.CheckList.Bind(wx.EVT_LEFT_DOWN, self.OnCheckListClicked)

        manualsizer = wx.BoxSizer(wx.VERTICAL)
        manualsizer.Add(self.CheckList, 0, wx.ALL, 3)

        self.SetSizerAndFit(manualsizer)
        self.Layout()

    def OnCheckListClicked(self, _):
        self.CheckList.SetSelection(wx.NOT_FOUND)

        sel = self.CheckList.HitTest(self.CheckList.ScreenToClient(wx.GetMousePosition()))

        if sel == wx.NOT_FOUND: return

        self.CheckList.Check(sel, not self.CheckList.IsChecked(sel))

    def OnDismiss(self):
        self.PowerSelector.Powers = [self.CheckList.GetString(i) for i in self.CheckList.GetCheckedItems()]

        wx.PostEvent(self.PowerSelector.Page, PowerSelectorChanged(wx.NewId(), control = self.PowerSelector))
        self.DestroyLater()
