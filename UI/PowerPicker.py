import wx
import re
import GameData
from Icon import GetIcon
from UI.ErrorControls import ErrorControlMixin
from Util.Incarnate import Rarities, Aliases

import wx.lib.newevent
PowerChanged, EVT_POWER_CHANGED = wx.lib.newevent.NewEvent()

class PowerPicker(ErrorControlMixin, wx.Button):
    def __init__(self, parent):
        wx.Button.__init__(self, parent)

        self.SetLabel('...')
        self.SetMinSize(wx.Size(-1, 40))
        self.Bind(wx.EVT_BUTTON, self.OnPowerPicker)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)
        self.Bind(EVT_POWER_CHANGED, self.OnPowerChanged)
        self.IconFilename = ''
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
        self.SetBitmapLabel(GetIcon('Powers', 'Empty'))
        wx.PostEvent(self, PowerChanged())

    def OnPowerChanged(self, _):
        self.Parent.Layout()


class PowerPickerMenu(wx.Menu):

    def __init__(self, button):
        wx.Menu.__init__(self)

        self.Button = button
        self.Bind(wx.EVT_MENU, self.OnMenuSelection)

    def BuildMenu(self):

        gen = wx.App.Get().Main.Profile.General

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
                        icon = GetIcon('Powers', powerset, power)
                        if icon:
                            menuitem.SetBitmap(icon)
                            setattr(menuitem, 'IconFilename', icon.Filename)
                        subsubmenu.Append(menuitem)
                    subitem = submenu.AppendSubMenu(subsubmenu, subsubname)
                    icon = GetIcon('Powers', powerset, subsubname)
                    if icon:
                        subitem.SetBitmap(icon)
                        setattr(subitem, 'IconFilename', icon.Filename)

                else:
                    menuitem = wx.MenuItem(id = wx.ID_ANY, text = power)
                    icon = GetIcon('Powers', powerset, power)
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

                powers = GameData.PoolPowers[poolname]
                for power in powers:
                    menuitem = wx.MenuItem(id = wx.ID_ANY, text = power)
                    icon = GetIcon('Powers', poolname,  power)
                    if icon:
                        menuitem.SetBitmap(icon)
                        setattr(menuitem, 'IconFilename', icon.Filename)
                    submenu.Append(menuitem)

        # Incarnate Powers
        menu = wx.Menu()
        for slot, slotdata in GameData.IncarnatePowers.items():
            submenu = wx.Menu()
            menu.AppendSubMenu(submenu, slot)
            for type in slotdata['Types']:
                subsubmenu = wx.Menu()
                submenu.AppendSubMenu(subsubmenu, type)

                for index, power in enumerate(slotdata['Powers']):
                    menuitem = wx.MenuItem(id = wx.ID_ANY, text = f"{type} {power}")
                    rarity = Rarities[ index ]

                    # aliases for the Lore types ie "Polar Lights" => "Lights" to match the icons
                    aliasedtype = Aliases.get(type, type)

                    if icon := GetIcon('Incarnate', f'Incarnate_{slot}_{aliasedtype}_{rarity}'):
                        menuitem.SetBitmap(icon)
                        setattr(menuitem, 'IconFilename', icon.Filename)

                    subsubmenu.Append(menuitem)
        self.AppendSubMenu(menu, "Incarnate")

        # Misc Powers
        submenu = self.MakeRecursiveMenu(GameData.MiscPowers)
        self.AppendSubMenu(submenu, "Misc")

    def MakeRecursiveMenu(self, menustruct):
        menu = wx.Menu()

        for name, data in menustruct.items():
            if isinstance(data, dict):
                submenu = self.MakeRecursiveMenu(data)
                menu.AppendSubMenu(submenu, name)
            elif isinstance(data, list):
                submenu = wx.Menu()
                for item in data:
                    item, iconlist = self.SplitNameAndIcon(item)
                    menuitem = wx.MenuItem(id = wx.ID_ANY, text = item)
                    icon = GetIcon('Powers', 'Misc', *iconlist)
                    if icon:
                        menuitem.SetBitmap(icon)
                        setattr(menuitem, 'IconFilename', icon.Filename)
                    submenu.Append(menuitem)
                menu.AppendSubMenu(submenu, name)

        return menu

    def OnMenuSelection(self, evt):
        menuitem = self.FindItemById(evt.GetId())
        label = menuitem.GetItemLabel()
        bitmap = menuitem.GetBitmapBundle()
        self.Button.SetLabel(label)
        self.Button.SetBitmap(bitmap)
        self.Button.IconFilename = getattr(menuitem, 'IconFilename')
        wx.PostEvent(self.Button, PowerChanged())

    def SplitNameAndIcon(self, namestr):
        if re.search(r'\|', namestr):
            name, iconstr = re.split(r'\|', namestr)
            iconlist = re.split(r'_', iconstr)
            return [name, iconlist]
        else:
            return [namestr, [namestr]]
