import wx
import re

import GameData
from Icon import GetIcon, SplitNameAndIcon
import UI
from UI.ErrorControls import ErrorControlMixin
from UI.ProfileAwareControl import ProfileAwareControlMixin
from Util.Incarnate import Rarities, Aliases
import wx.lib.agw.flatmenu as FM

import wx.lib.newevent
PowerChanged, EVT_POWERPICKER_CHANGED = wx.lib.newevent.NewCommandEvent()

class PowerPicker(ProfileAwareControlMixin, ErrorControlMixin, wx.Button):
    def __init__(self, parent, menuclass = None, size = wx.DefaultSize) -> None:
        super().__init__(parent, size = size)

        if size == wx.DefaultSize:
            self.SetMinSize(wx.Size(-1, 40))
        self.Bind(wx.EVT_BUTTON,     self.OnPowerPicker)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)
        self.IconFilename = ''
        self.PickerClass = menuclass # for JIT instantiation of custom menu.  Yes this is necessary
        self.Picker = None # stash the actual menu here once we on-demand create it, in OnPowerPicker
        self.SetFont(UI.COHFont())
        if self.Picker:  # we've passed in our own menu, bind its behavior
            self.Picker.Bind(wx.EVT_MENU, self.OnMenuSelected)

    def HasPowerPicked(self) -> str:
        if self.GetLabel():
            return self.GetLabel()
        else:
            return ''

    def OnPowerPicker(self, _) -> None:
        # if we didn't pass in a menu, make the normal full-on one
        if self.PickerClass:
            picker = self.PickerClass()
        else:
            picker = PowerPickerMenu(self)
            picker.BuildMenu()
        picker.Bind(wx.EVT_MENU, self.OnMenuSelected)
        self.Picker = picker
        picker.Popup(wx.GetMousePosition())

    def OnRightClick(self, _) -> None:
        self.SetLabel('')
        self.IconFilename = ''
        self.SetBitmapLabel(GetIcon('Empty'))
        self.OnMenuSelected()

    def doOnMenuSelected(self, evt = None) -> None:
        if evt:
            menu = evt.GetEventObject()
            menuitem = menu.FindItem(evt.GetId())
            label = menuitem.GetLabel()
            bitmap = menuitem.GetBitmap()
            self.SetLabel(label)
            self.SetBitmap(bitmap)
            self.IconFilename = menuitem.IconFilename

    def OnMenuSelected(self, evt = None) -> None:
        self.doOnMenuSelected(evt)
        wx.PostEvent(self, PowerChanged(wx.NewId(), control = self))

    # DRYed this up from a few places.  Probably belongs here but not 100% sure.
    def SetIconFromFilename(self, filename):
        # this dance is to support Profiles saved pre-PIL icons
        if re.match('Powers_', filename):
            filename = re.sub('^Powers_', '', filename)
            icon = GetIcon('Powers', filename)
        else:
            filename = re.sub(r'\.png$', '', filename, flags = re.IGNORECASE)
            start, *bits = re.split(r'[\\/]', filename)
            if start != 'Powers':
                wx.LogError(f'Got a very strange picon value: "{filename}" - this is a bug!')
                icon = GetIcon('Empty')
            else:
                icon = GetIcon('Powers', *bits)
        self.IconFilename = filename
        self.SetBitmap(icon)

    def GetValue(self):
        return {
            'power'    : self.GetLabel(),
            'iconfile' : self.IconFilename,
        }

    def SetValue(self, value):
        self.SetLabel(value.get('power', ''))
        if iconfile := value.get('iconfile'):
            self.IconFilename = iconfile
            self.SetIconFromFilename(iconfile)

class PowerPickerMenu(FM.FlatMenu):
    def __init__(self, parent):
        super().__init__(parent)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, parent.OnMenuSelected)

    def SetSize(self, size):
        # add 20 to our height iff we are MacOS pre-fix
        if not isinstance(self, wx.PopupWindow):
            size.SetHeight(size.GetHeight() + 20)
        super().SetSize(size)

    def BuildMenu(self) -> None:
        gen = self.Profile.General

        # primary / secondary / epic powers
        archdata = GameData.Archetypes[gen.GetState('Archetype')]
        for category in ['Primary', 'Secondary', 'Epic']:
            submenu = PowerPickerMenu(self.Parent)
            powerset = gen.GetState(category)
            if not powerset: continue
            self.AppendSubMenu(submenu, f"{category}: {powerset}")

            powers = archdata[category][powerset]
            for power in powers:
                if isinstance(power, dict):  # for sub sub menus like Corruptor -> Dual Pistols -> Swap Ammo
                    [(subsubname, items)] = power.items()
                    subsubmenu = PowerPickerMenu(self.Parent)
                    for power in items:
                        if not self.ShowPower(category, power): continue
                        icon = GetIcon('Powers', f'{powerset}_{power}')
                        menuitem = PowerMenuItem(self, power, icon)
                        subsubmenu.AppendItem(menuitem)
                    subitem = submenu.AppendSubMenu(subsubmenu, subsubname)
                    # little bit of wx.Font hoop-jumping just for this corner case, sigh
                    subitem.SetFont(UI.COHFont())
                    icon = GetIcon('Powers', f'{powerset}_{subsubname}')
                    if icon:
                        subitem.SetNormalBitmap(icon.GetBitmap(wx.Size(32,32)))

                else:
                    if not self.ShowPower(category, power): continue
                    icon = GetIcon('Powers', f'{powerset}_{power}')
                    menuitem = PowerMenuItem(self, power, icon)
                    submenu.AppendItem(menuitem)

        # Pool powers
        for poolpicker in ["Pool1", "Pool2", "Pool3", "Pool4"]:
            poolname = gen.GetState(poolpicker)
            if poolname:
                submenu = PowerPickerMenu(self.Parent)
                self.AppendSubMenu(submenu, "Pool: " + poolname)

                powers = GameData.PoolPowers[poolname]
                for power in powers:
                    if not self.ShowPower(poolpicker, power): continue
                    icon = GetIcon('Powers', f'{poolname}_{power}')
                    menuitem = PowerMenuItem(self, power, icon)
                    submenu.AppendItem(menuitem)

        # Incarnate Powers
        menu = PowerPickerMenu(self.Parent)
        for slot, slotdata in GameData.IncarnatePowers.items():
            if 'Powers' in slotdata:
                submenu = PowerPickerMenu(self.Parent)
                menu.AppendSubMenu(submenu, slot)
                for inc_type in slotdata['Types']:
                    subsubmenu = PowerPickerMenu(self.Parent)
                    submenu.AppendSubMenu(subsubmenu, inc_type)

                    for index, power in enumerate(slotdata['Powers']):
                        rarity = Rarities[ index ]

                        # aliases for the Lore types ie "Polar Lights" => "Lights" to match the icons
                        aliasedtype = Aliases.get(inc_type, inc_type)

                        icon = GetIcon('Incarnate', f'{slot}_{aliasedtype}_{rarity}')
                        menuitem = PowerMenuItem(self, f"{inc_type} {power}", icon)
                        subsubmenu.AppendItem(menuitem)
        self.AppendSubMenu(menu, "Incarnate")

        # Misc Powers
        submenu = self.MakeRecursiveMenu(GameData.MiscPowers)
        self.AppendSubMenu(submenu, "Misc")

    def ShowPower(self, category:str, power:str) -> bool:
        # This next line is uuuuugly.  What is the right way to do this?
        # Answer:  a method on General?  On Profile?
        powerlist = self.Profile.General.Ctrls[f'{category}Powers'].GetValue()
        if   powerlist == []    : return True # we haven't picked powers, show them all
        elif power in powerlist : return True # we have picked this one, show it
        else                    : return False

    def MakeRecursiveMenu(self, menustruct) -> FM.FlatMenu:

        menu = PowerPickerMenu(self.Parent)

        for name, data in menustruct.items():
            if isinstance(data, dict):
                submenu = self.MakeRecursiveMenu(data)
                menu.AppendSubMenu(submenu, name)
            elif isinstance(data, list):
                submenu = PowerPickerMenu(self.Parent)
                for item in data:
                    item, iconpathparts = SplitNameAndIcon(item)
                    icon = GetIcon('Powers', f'Misc_{iconpathparts[0]}')
                    menuitem = PowerMenuItem(self, item, icon)
                    submenu.AppendItem(menuitem)
                menu.AppendSubMenu(submenu, name)

        return menu

class PowerMenuItem(FM.FlatMenuItem):
    def __init__(self, parent, text, icon = None):
        icon = icon or GetIcon('Empty')
        super().__init__(parent, id = wx.ID_ANY, kind = wx.ITEM_NORMAL,
             label = text, normalBmp = icon.GetBitmap(wx.Size(32,32)))

        self.IconFilename = icon.Filename if icon else ''

        self.SetFont(UI.COHFont())
