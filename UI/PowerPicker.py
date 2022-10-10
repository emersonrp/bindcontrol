import wx
import GameData
from Utility import Icon

class PowerPicker(wx.Button):
    def __init__(self, parent):
        wx.Button.__init__(self, parent)

        self.SetLabel('...')
        self.SetMinSize((-1, 40))
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
            powerset = gen.GetState(category)
            if not powerset: continue
            self.AppendSubMenu(submenu, f"{category}: {powerset}")

            powers = archdata[category][powerset]
            for power in powers:
                menuitem = wx.MenuItem(id = wx.ID_ANY, text = power)
                icon = Icon(powerset = powerset, power = power)
                if icon: menuitem.SetBitmap(icon)
                submenu.Append(menuitem)

        # Pool powers
        for poolpicker in ["Pool1", "Pool2", "Pool3", "Pool4"]:
            poolname = gen.GetState(poolpicker)
            if poolname:
                submenu = wx.Menu()
                self.AppendSubMenu(submenu, "Pool: " + poolname)

                powers = GameData.MiscPowers['Pool'][poolname]
                for power in powers:
                    menuitem = wx.MenuItem(id = wx.ID_ANY, text = power)
                    icon = Icon(powerset = poolname, power = power)
                    if icon: menuitem.SetBitmap(icon)
                    submenu.Append(menuitem)


    def OnMenuSelection(self, evt):
        menuitem = self.FindItemById(evt.GetId())
        label = menuitem.GetItemLabel()
        bitmap = menuitem.GetBitmapBundle()
        self.Button.SetLabel(label)
        self.Button.SetBitmap(bitmap)

