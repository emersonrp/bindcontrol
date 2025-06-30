import wx
import re
from Icon import GetIcon

import GameData

class IncarnateBox(wx.StaticBoxSizer):
    def __init__(self, parent):
        wx.StaticBoxSizer.__init__(self, wx.HORIZONTAL, parent, 'Incarnate Powers')

        staticbox = self.GetStaticBox()
        self.Profile = parent.Profile

        incarnateSizer = wx.GridBagSizer(4, 4)

        self.Add(incarnateSizer, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 6)

        server = self.Profile.Server

        if server == "Rebirth":
            self.genesisInc = IncarnatePicker(staticbox, profile = self.Profile, label = "Genesis")

        self.hybridInc    = IncarnatePicker(staticbox, profile = self.Profile, label = "Hybrid")
        self.loreInc      = IncarnatePicker(staticbox, profile = self.Profile, label = "Lore")
        self.destinyInc   = IncarnatePicker(staticbox, profile = self.Profile, label = "Destiny")
        self.judgementInc = IncarnatePicker(staticbox, profile = self.Profile, label = "Judgement")
        self.interfaceInc = IncarnatePicker(staticbox, profile = self.Profile, label = "Interface")
        self.alphaInc     = IncarnatePicker(staticbox, profile = self.Profile, label = "Alpha")

        if server == "Rebirth":
            incarnateSizer.Add(self.hybridInc,    [0,0], [1,2], wx.EXPAND|wx.LEFT, 12)
            incarnateSizer.Add(self.genesisInc,   [0,2], [1,2], wx.EXPAND|wx.RIGHT, 12)
        else:
            incarnateSizer.Add(self.hybridInc,    [0,1], [1,2], wx.EXPAND)

        incarnateSizer.Add(self.loreInc,      [1,0], [1,2], wx.EXPAND|wx.LEFT, 12)
        incarnateSizer.Add(self.destinyInc,   [1,2], [1,2], wx.EXPAND|wx.RIGHT, 12)
        incarnateSizer.Add(self.judgementInc, [2,0], [1,2], wx.EXPAND|wx.LEFT, 12)
        incarnateSizer.Add(self.interfaceInc, [2,2], [1,2], wx.EXPAND|wx.RIGHT, 12)
        incarnateSizer.Add(self.alphaInc,     [3,1], [1,2], wx.EXPAND|wx.BOTTOM, 12)

        incarnateSizer.AddGrowableCol(0)
        incarnateSizer.AddGrowableCol(1)
        incarnateSizer.AddGrowableCol(2)
        incarnateSizer.AddGrowableCol(3)

    def GetPowers(self):
        server = self.Profile.Server
        powers = []

        boxes = [self.hybridInc, self.loreInc, self.destinyInc, self.judgementInc, self.interfaceInc, self.alphaInc]
        if server == "Rebirth":
            boxes.append(self.genesisInc)

        for box in boxes:
            name = box.IncName.GetLabel()
            if name:
                powers.append({
                    'name'         : name,
                    'icon'         : box.IncIcon.GetBitmapLabel(),
                    'iconfilename' : box.IconFilename,
                })
        return powers

    def FillWith(self, data):
        incarnate = data['General'].get('Incarnate', None)
        if incarnate:
            for boxname, contents in incarnate.items():
                box = getattr(self, boxname.lower() + "Inc", None)
                if box:
                    box.IncName.SetLabel(contents['power'])
                    box.IncIcon.SetBitmapLabel(GetIcon(contents['iconfile']))
                    box.IconFilename = contents['iconfile']

    def GetData(self):
        incarnatedata = {}
        server = self.Profile.Server

        boxes = [self.hybridInc, self.loreInc, self.destinyInc, self.judgementInc, self.interfaceInc, self.alphaInc]
        if server == "Rebirth":
            boxes.append(self.genesisInc)

        for box in boxes:
            if box.IncName.GetLabel():
                incarnatedata[box.Label] = {
                    'power'    : re.sub('\n', ' ', box.IncName.GetLabel()),
                    'iconfile' : box.IconFilename,
                }
        return incarnatedata

import wx.lib.buttons as buttons
class IncarnatePicker(wx.StaticBoxSizer):
    def __init__(self, parent, profile, label = ""):
        wx.StaticBoxSizer.__init__(self, wx.HORIZONTAL, parent, label = label)
        staticbox = self.GetStaticBox()

        self.Profile = profile
        self.Label = label
        self.IconFilename = ''
        self.PopupMenu = None

        hsizer = wx.BoxSizer(wx.HORIZONTAL)

        self.IncIcon = buttons.ThemedGenBitmapButton(staticbox, bitmap = GetIcon('Empty'), size=wx.Size(39,40))
        setattr(self.IncIcon, 'Picker', self)
        self.IncIcon.Bind(wx.EVT_BUTTON, self.OnButtonPress)
        self.IncIcon.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)
        self.IncName = wx.StaticText(staticbox, wx.ID_ANY, style=wx.ALIGN_RIGHT)

        hsizer.Add(self.IncName, 1, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 6)
        hsizer.Add(self.IncIcon, 0, wx.ALIGN_CENTER_VERTICAL)

        self.Add(hsizer, 1, wx.EXPAND|wx.RIGHT|wx.BOTTOM, 12)

    def OnButtonPress(self, evt):
        button = evt.EventObject
        if not self.PopupMenu:
            self.PopupMenu = self.BuildMenu(self.Label)
            self.PopupMenu.Bind(wx.EVT_MENU, self.OnMenuSelection)

        button.PopupMenu(self.PopupMenu)

    def OnMenuSelection(self, evt):
        menuitem = evt.EventObject.FindItemById(evt.GetId())

        self.IncName.SetLabel(menuitem.GetItemLabel())
        self.IncIcon.SetBitmapLabel(menuitem.GetBitmapBundle().GetBitmap(wx.Size(32,32)))
        self.IconFilename = menuitem.IconFilename

        self.Profile.SetModified()

        # Yes both of the self.Layout() are necessary to do the sizing / wrap dance.
        self.Layout()
        w,_ = self.IncName.GetSize()
        self.IncName.Wrap(w)
        self.Layout()
        evt.Skip()

    def OnRightClick(self, evt):
        button = evt.EventObject
        button.SetBitmapLabel(GetIcon('Empty'))
        button.Picker.IncName.SetLabel('')
        button.Layout()
        evt.Skip()

    def BuildMenu(self, slot):
        menu = wx.Menu()

        incData = GameData.IncarnatePowers[slot]

        for type in incData['Types']:
            submenu = wx.Menu()
            menu.AppendSubMenu(submenu, type)

            for index, power in enumerate(incData['Powers']):
                menuitem = wx.MenuItem(id = wx.ID_ANY, text = f"{type} {power}")
                rarity = Rarities[ index ]

                # aliases for the Lore types ie "Polar Lights" => "Lights" to match the icons
                aliasedtype = Aliases.get(type, type)

                iconname = f"Incarnate/Incarnate_{slot}_{aliasedtype}_{rarity}"
                icon = GetIcon(iconname)
                if icon: menuitem.SetBitmap(icon)
                setattr(menuitem, 'IconFilename', iconname)

                submenu.Append(menuitem)

        return menu

Rarities = ['Common', 'Uncommon', 'Uncommon', 'Rare', 'Rare', 'Rare', 'Rare', 'VeryRare', 'VeryRare']
Aliases = {
    "Banished Pantheon"   : "Banished",
    "Carnival of Shadows" : "Carnival",
    "Cimerorans"          : "Cimeroran",
    "Knives of Vengeance" : "Knives",
    "Phantom"             : "Phantoms",
    "Polar Lights"        : "Lights",
    "Robotic Drones"      : "Drones",
    "Storm Elementals"    : "Elementals",
    "Talons of Vengeance" : "Talons",
    "Warworks"            : "WarWorks",
}
