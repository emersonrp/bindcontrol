import wx
import GameData
from Icon import GetIcon, SplitNameAndIcon
from UI.ErrorControls import ErrorControlMixin
from Util.Incarnate import Rarities, Aliases

import wx.lib.newevent
PowerChanged, EVT_POWERPICKER_CHANGED = wx.lib.newevent.NewCommandEvent()

class PowerPicker(ErrorControlMixin, wx.Button):
    def __init__(self, parent, menu = None, size = wx.DefaultSize) -> None:
        super().__init__(parent, size = size)

        if size == wx.DefaultSize:
            self.SetMinSize(wx.Size(-1, 40))
        self.Bind(wx.EVT_BUTTON, self.OnPowerPicker)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)
        self.IconFilename = ''
        self.Picker = menu
        if self.Picker:  # we've passed in our own menu, bind its behavior
            self.Picker.Bind(wx.EVT_MENU, self.OnMenuSelected)

    def HasPowerPicked(self) -> str:
        if self.GetLabel():
            return self.GetLabel()
        else:
            return ''

    def OnPowerPicker(self, _) -> None:
        # if we didn't pass in a menu, make the normal full-on one
        if self.Picker:
            picker = self.Picker
        else:
            picker = PowerPickerMenu()
            picker.Bind(wx.EVT_MENU, self.OnMenuSelected)
            picker.BuildMenu()
        self.PopupMenu(picker)
        # TODO maybe it should update itself with the results from the menu
        # instead of the menu reaching in and fiddling with it.  Maybe.
        #
        # TODO 2:  now that we possibly pass in our own menu, that's not
        # quite as simple as all that.  Still, it seems more The Right Way.

    def OnRightClick(self, _) -> None:
        self.SetLabel('')
        self.IconFilename = ''
        self.SetBitmapLabel(GetIcon('Empty'))
        self.OnMenuSelected()

    def doOnMenuSelected(self, evt = None) -> None:
        if evt:
            menu = evt.GetEventObject()
            menuitem = menu.FindItemById(evt.GetId())
            label = menuitem.GetItemLabel()
            bitmap = menuitem.GetBitmapBundle()
            self.SetLabel(label)
            self.SetBitmap(bitmap)
            self.IconFilename = getattr(menuitem, 'IconFilename')

    def OnMenuSelected(self, evt = None) -> None:
        self.doOnMenuSelected(evt)
        wx.PostEvent(self, PowerChanged(wx.NewId(), control = self))

class PowerPickerMenu(wx.Menu):
    def BuildMenu(self) -> None:

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
                        if not self.ShowPower(category, power): continue
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
                    if not self.ShowPower(category, power): continue
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
                    if not self.ShowPower(poolpicker, power): continue
                    menuitem = wx.MenuItem(id = wx.ID_ANY, text = power)
                    icon = GetIcon('Powers', poolname,  power)
                    if icon:
                        menuitem.SetBitmap(icon)
                        setattr(menuitem, 'IconFilename', icon.Filename)
                    submenu.Append(menuitem)

        # Incarnate Powers
        menu = wx.Menu()
        for slot, slotdata in GameData.IncarnatePowers.items():
            if 'Powers' in slotdata:
                submenu = wx.Menu()
                menu.AppendSubMenu(submenu, slot)
                for inc_type in slotdata['Types']:
                    subsubmenu = wx.Menu()
                    submenu.AppendSubMenu(subsubmenu, inc_type)

                    for index, power in enumerate(slotdata['Powers']):
                        menuitem = wx.MenuItem(id = wx.ID_ANY, text = f"{inc_type} {power}")
                        rarity = Rarities[ index ]

                        # aliases for the Lore types ie "Polar Lights" => "Lights" to match the icons
                        aliasedtype = Aliases.get(inc_type, inc_type)

                        if icon := GetIcon('Incarnate', f'Incarnate_{slot}_{aliasedtype}_{rarity}'):
                            menuitem.SetBitmap(icon)
                            setattr(menuitem, 'IconFilename', icon.Filename)

                        subsubmenu.Append(menuitem)
        self.AppendSubMenu(menu, "Incarnate")

        # Misc Powers
        submenu = self.MakeRecursiveMenu(GameData.MiscPowers)
        self.AppendSubMenu(submenu, "Misc")

    def ShowPower(self, category:str, power:str) -> bool:
        # This next line is uuuuugly.  What is the right way to do this?
        powerlist = wx.App.Get().Main.Profile.General.Ctrls[f'{category}Powers'].GetValue()
        if   powerlist == []    : return True # we haven't picked powers, show them all
        elif power in powerlist : return True # we have picked this one, show it
        else                    : return False

    def MakeRecursiveMenu(self, menustruct) -> wx.Menu:
        menu = wx.Menu()

        for name, data in menustruct.items():
            if isinstance(data, dict):
                submenu = self.MakeRecursiveMenu(data)
                menu.AppendSubMenu(submenu, name)
            elif isinstance(data, list):
                submenu = wx.Menu()
                for item in data:
                    item, iconpathparts = SplitNameAndIcon(item)
                    menuitem = wx.MenuItem(id = wx.ID_ANY, text = item)
                    icon = GetIcon('Powers', 'Misc', *iconpathparts)
                    if icon:
                        menuitem.SetBitmap(icon)
                        setattr(menuitem, 'IconFilename', icon.Filename)
                    submenu.Append(menuitem)
                menu.AppendSubMenu(submenu, name)

        return menu
