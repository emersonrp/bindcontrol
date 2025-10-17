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
        #powerlist.CheckList.SetSelection(wx.NOT_FOUND)

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

        manualsizer = wx.BoxSizer(wx.VERTICAL)

        self.Popups = []
        for power in powers:
            popuppower = PopupPower(self, powerset, power)
            popuppower.CB.SetValue(power in self.PowerSelector.Powers)
            manualsizer.Add(popuppower, 0)
            self.Popups.append(popuppower)

        self.SetSizerAndFit(manualsizer)
        self.Layout()

    def OnDismiss(self):
        self.PowerSelector.Powers = [p.Power for p in self.Popups if p.CB.IsChecked()]

        wx.PostEvent(self.PowerSelector.Page, PowerSelectorChanged(wx.NewId(), control = self.PowerSelector))
        self.DestroyLater()

class PopupPower(wx.Panel):
    def __init__(self, parent, powerset, power):
        super().__init__(parent)
        self.Power = power

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.CB = wx.CheckBox(self)
        sizer.Add(self.CB, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3)

        icon = wx.GenericStaticBitmap(self, bitmap = GetIcon('Powers', powerset, power), size = wx.Size(16,16))
        icon.SetScaleMode(wx.GenericStaticBitmap.Scale_AspectFill)
        sizer.Add(icon, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3)

        text = wx.StaticText(self, label = power)
        sizer.Add(text, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3)

        self.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
        icon.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
        text.Bind(wx.EVT_LEFT_DOWN, self.OnClick)

        self.SetSizerAndFit(sizer)

    def OnClick(self, evt = None):
        if evt: evt.Skip()
        self.CB.SetValue(not self.CB.IsChecked())
