import wx
import GameData

class PowerPicker(wx.Button):
    def __init__(self, parent):
        wx.Button.__init__(self, parent)

        self.SetLabel('...')
        self.Bind(wx.EVT_BUTTON, self.OnPowerPicker)

    def OnPowerPicker(self, _):
        self.Picker = PowerPickerMenu(self)
        self.Picker.BuildMenu()
        self.PopupMenu(self.Picker)

class PowerPickerMenu(wx.Menu):

    def __init__(self, button):
        wx.Menu.__init__(self)

        self.Button = button
        self.Bind(wx.EVT_MENU, self.OnMenuSelection)

    def BuildMenu(self):

        profile = wx.Window.FindWindowByName("Profile")
        gen = profile.General

        # primary / secondary / epic powers
        archdata = GameData.Archetypes[gen.GetState('Archetype')]
        for category in ['Primary', 'Secondary', 'Epic']:
            submenu = wx.Menu()
            catname = gen.GetState(category)
            self.AppendSubMenu(submenu, f"{category}: {catname}")

            powers = archdata[category][gen.GetState(category)]

            for power in powers:
                submenu.Append(-1, power)

        # Pool powers
        for poolpicker in ["Pool1", "Pool2", "Pool3", "Pool4"]:
            poolname = gen.GetState(poolpicker)
            if poolname:
                submenu = wx.Menu()
                self.AppendSubMenu(submenu, "Pool: " + poolname)

    def OnMenuSelection(self, evt):
        menuitem = self.FindItemById(evt.GetId())
        label = menuitem.GetItemLabel()
        self.Button.SetLabel(label)

