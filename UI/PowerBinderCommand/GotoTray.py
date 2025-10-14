import wx
from UI.PowerBinderCommand import PowerBinderCommand

####### Unselect
class GotoTray(PowerBinderCommand):
    Name = "Set Hotbar To Power Tray"
    Menu = "Graphics / UI"

    def BuildUI(self, dialog) -> wx.BoxSizer:
        CenteringSizer = wx.BoxSizer(wx.VERTICAL)
        MainSizer = wx.FlexGridSizer(2, 5, 5)

        MainSizer.Add(wx.StaticText(dialog, label = "Set Hotbar:"), 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        choices = ['1', '2', '3', '4'] if self.Profile.Server() == "Rebirth" else ['1', '2', '3']
        self.HotbarPicker = wx.Choice(dialog, choices = choices)
        self.HotbarPicker.SetSelection(0)
        MainSizer.Add(self.HotbarPicker, 1, wx.ALIGN_CENTER_VERTICAL)

        MainSizer.Add(wx.StaticText(dialog, label = "To Power Tray:"), 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        choices = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.TrayPicker = wx.Choice(dialog, choices = choices)
        self.TrayPicker.SetSelection(0)
        MainSizer.Add(self.TrayPicker, 1, wx.ALIGN_CENTER_VERTICAL)

        CenteringSizer.Add(MainSizer, flag = wx.ALIGN_CENTER)
        return CenteringSizer

    def MakeBindString(self) -> str:
        bar = self.HotbarPicker.GetStringSelection()
        tray = self.TrayPicker.GetStringSelection()
        return f"gototraystray {bar} {tray}"

    def Serialize(self) -> dict:
        return {
            'bar' : self.HotbarPicker.GetStringSelection(),
            'tray' : self.TrayPicker.GetStringSelection(),
        }

    def Deserialize(self, init) -> None:
        self.HotbarPicker.SetStringSelection(init.get('bar', '1'))
        self.TrayPicker.SetStringSelection(init.get('tray', '1'))
