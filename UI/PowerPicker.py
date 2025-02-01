import wx
import GameData
from Icon import GetIcon
from UI.ErrorControls import ErrorControlMixin

import wx.lib.newevent
PowerChanged, EVT_POWER_CHANGED = wx.lib.newevent.NewEvent()

class PowerPicker(ErrorControlMixin, wx.Button):
    def __init__(self, parent):
        wx.Button.__init__(self, parent)

        self.SetLabel('...')
        self.SetMinSize((-1, 40))
        self.Bind(wx.EVT_BUTTON, self.OnPowerPicker)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)
        self.IconFilename = ''
        self.Errors = {}
        self.Warnings = {}
        self.DefaultToolTip = ""
        self.Picker = None

    def OnPowerPicker(self, _):
        self.Picker = PowerPickerMenu(self)
        self.Picker.BuildMenu()
        self.PopupMenu(self.Picker)
        # TODO maybe it should update itself with the results from the menu
        # instead of the menu reaching in and fiddling with it.  Maybe.

    def OnRightClick(self, _):
        self.SetLabel('...')
        self.IconFilename = ''
        self.SetBitmapLabel(GetIcon('Empty'))
        wx.PostEvent(self, PowerChanged())

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
                if isinstance(power, dict):
                    [(subsubname, items)] = power.items()
                    subsubmenu = wx.Menu()
                    for power in items:
                        menuitem = wx.MenuItem(id = wx.ID_ANY, text = power)
                        icon = GetIcon(powerset = powerset, power = power)
                        if icon:
                            menuitem.SetBitmap(icon)
                            setattr(menuitem, 'IconFilename', icon.Filename)
                        subsubmenu.Append(menuitem)
                    subitem = submenu.AppendSubMenu(subsubmenu, subsubname)
                    icon = GetIcon(powerset = powerset, power = subsubname)
                    if icon:
                        subitem.SetBitmap(icon)
                        setattr(subitem, 'IconFilename', icon.Filename)

                else:
                    menuitem = wx.MenuItem(id = wx.ID_ANY, text = power)
                    icon = GetIcon(powerset = powerset, power = power)
                    if icon:
                        menuitem.SetBitmap(icon)
                        setattr(menuitem, 'IconFilename', icon.Filename)
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
                    icon = GetIcon(powerset = poolname, power = power)
                    if icon:
                        menuitem.SetBitmap(icon)
                        setattr(menuitem, 'IconFilename', icon.Filename)
                    submenu.Append(menuitem)

        # Incarnate Powers
        submenu = wx.Menu()
        incPowers = gen.IncarnateBox.GetPowers()
        if incPowers:
            self.AppendSubMenu(submenu, "Incarnate")
            for power in incPowers:
                menuitem = wx.MenuItem(id = wx.ID_ANY, text = power['name'])
                icon = power['icon']
                if icon:
                    menuitem.SetBitmap(icon)
                    setattr(menuitem, 'IconFilename', power['iconfilename'])
                submenu.Append(menuitem)

        # Misc / Inherent Powers
        submenu = wx.Menu()
        self.AppendSubMenu(submenu, "Misc")

        accoladepowers = GameData.MiscPowers['Badge']['Accolade']
        if accoladepowers:
            accolademenu = wx.Menu()
            submenu.AppendSubMenu(accolademenu, "Accolade")
            for power in accoladepowers:
                menuitem = wx.MenuItem(id = wx.ID_ANY, text = power)
                icon = GetIcon(powerset = 'Misc', power = power)
                if icon:
                    menuitem.SetBitmap(icon)
                    setattr(menuitem, 'IconFilename', icon.Filename)
                accolademenu.Append(menuitem)

        inherentpowers = GameData.MiscPowers['General']['Inherent']
        if inherentpowers:
            inherentmenu = wx.Menu()
            submenu.AppendSubMenu(inherentmenu, "Inherent")
            for power in inherentpowers:
                menuitem = wx.MenuItem(id = wx.ID_ANY, text = power)
                icon = GetIcon(powerset = 'Misc', power = power)
                if icon:
                    menuitem.SetBitmap(icon)
                    setattr(menuitem, 'IconFilename', icon.Filename)
                inherentmenu.Append(menuitem)

        smartpowers = GameData.MiscPowers['General']['SMART']
        if smartpowers:
            smartmenu = wx.Menu()
            submenu.AppendSubMenu(smartmenu, "SMART")
            for power in smartpowers:
                menuitem = wx.MenuItem(id = wx.ID_ANY, text = power)
                icon = GetIcon(powerset = 'Misc', power = power)
                if icon:
                    menuitem.SetBitmap(icon)
                    setattr(menuitem, 'IconFilename', icon.Filename)
                smartmenu.Append(menuitem)

    def OnMenuSelection(self, evt):
        menuitem = self.FindItemById(evt.GetId())
        label = menuitem.GetItemLabel()
        bitmap = menuitem.GetBitmapBundle()
        self.Button.SetLabel(label)
        self.Button.SetBitmap(bitmap)
        self.Button.IconFilename = menuitem.IconFilename
        wx.PostEvent(self.Button, PowerChanged())
