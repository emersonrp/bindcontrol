import wx
import GameData

def OnPowerPicker(evt):
    button = evt.EventObject

    picker = PowerPicker(button)
    picker.BuildMenu()
    button.PopupMenu(picker)

class PowerPicker(wx.Menu):

    def __init__(self, target):
        wx.Menu.__init__(self)

        self.UpdateTarget = target
        self.Bind(wx.EVT_MENU, self.OnMenuSelection)

    def BuildMenu(self):

        profile = wx.Window.FindWindowByName("Profile")
        gen = profile.General

        archdata = GameData.Archetypes[gen.GetState('Archetype')]
        for category in ['Primary', 'Secondary', 'Epic']:
            submenu = wx.Menu()
            catname = gen.GetState(category)
            self.AppendSubMenu(submenu, f"{category}: {catname}")

            powers = archdata[category][gen.GetState(category)]

            for power in powers:
                submenu.Append(-1, power)

    def OnMenuSelection(self, evt):
        menuitem = self.FindItemById(evt.GetId())
        label = menuitem.GetItemLabel()
        self.UpdateTarget.SetLabel(label)
