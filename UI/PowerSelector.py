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

        # a whole wx.Panel just to give us a two-pixel "3D Shadow" border to make it look like a menu
        borderpanel = wx.Panel(self)
        borderpanel.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))
        bordersizer = wx.BoxSizer(wx.VERTICAL)

        # And another wx.Panel to put all the "menu items" on that's menu-colored
        powerpanel = wx.Panel(borderpanel)
        powerpanel.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU))
        powersizer = wx.BoxSizer(wx.VERTICAL)
        powersizer.Add(wx.StaticText(powerpanel, label = powerset), 0, wx.ALL|wx.ALIGN_CENTER, 5)
        powersizer.Add(wx.StaticLine(powerpanel, style = wx.HORIZONTAL), 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)

        self.Popups = []
        for power in powers:
            popuppower = PopupPower(powerpanel, powerset, power)
            popuppower.CB.SetValue(power in self.PowerSelector.Powers)
            powersizer.Add(popuppower, 0, wx.EXPAND)
            self.Popups.append(popuppower)

        powerpanel.SetSizerAndFit(powersizer)

        # shim the power panel into the main sizer with a 2px border
        bordersizer.Add(borderpanel, 1, wx.EXPAND|wx.ALL, 2)

        self.SetSizerAndFit(bordersizer)
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

        self.PowerText = wx.StaticText(self, label = power)
        sizer.Add(self.PowerText, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3)

        self.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
        icon.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
        self.PowerText.Bind(wx.EVT_LEFT_DOWN, self.OnClick)

        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnterWindow)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)

        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU))
        self.PowerText.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENUTEXT))

        self.SetSizerAndFit(sizer)

    def OnClick(self, evt):
        evt.Skip()
        self.CB.SetValue(not self.CB.IsChecked())

    def OnEnterWindow(self, evt):
        evt.Skip()
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENUHILIGHT))
        self.PowerText.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))

    def OnLeaveWindow(self, evt):
        evt.Skip()
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU))
        self.PowerText.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENUTEXT))
