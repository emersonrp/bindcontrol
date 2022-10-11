import wx
from Utility import Icon

import GameData

class IncarnateBox(wx.StaticBoxSizer):
    def __init__(self, parent):
        wx.StaticBoxSizer.__init__(self, wx.HORIZONTAL, parent, 'Incarnate Powers')

        staticbox = self.GetStaticBox()

        incarnateSizer = wx.GridBagSizer(4, 4)

        self.Add(incarnateSizer, 1, wx.EXPAND|wx.ALL, 6)

        self.hybridInc    = IncarnatePicker(staticbox, label = "Hybrid")
        self.loreInc      = IncarnatePicker(staticbox, label = "Lore")
        self.destinyInc   = IncarnatePicker(staticbox, label = "Destiny")
        self.judgementInc = IncarnatePicker(staticbox, label = "Judgement")
        self.interfaceInc = IncarnatePicker(staticbox, label = "Interface")
        self.alphaInc     = IncarnatePicker(staticbox, label = "Alpha")

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

class IncarnatePicker(wx.StaticBoxSizer):
    def __init__(self, parent, label = ""):
        wx.StaticBoxSizer.__init__(self, wx.HORIZONTAL, parent, label = label)
        staticbox = self.GetStaticBox()

        self.Label = label
        self.PopupMenu = self.BuildMenu(label)
        self.PopupMenu.Bind(wx.EVT_MENU, self.OnMenuSelection)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)

        self.IncIcon = wx.Button(staticbox, size=wx.Size(60,40))
        self.IncIcon.Bind(wx.EVT_BUTTON, self.OnButtonPress)
        self.IncName = wx.StaticText(staticbox, wx.ID_ANY, style=wx.ALIGN_RIGHT)

        hsizer.Add(self.IncName, 1, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 6)
        hsizer.Add(self.IncIcon, 0, wx.ALIGN_CENTER_VERTICAL)

        self.Add(hsizer, 1, wx.EXPAND|wx.RIGHT|wx.BOTTOM, 12)

    def OnButtonPress(self, evt):
        button = evt.EventObject

        button.PopupMenu(self.PopupMenu)

    def OnMenuSelection(self, evt):
        menuitem = evt.EventObject.FindItemById(evt.GetId())

        self.IncName.SetLabel(menuitem.GetItemLabel())
        self.IncIcon.SetBitmapLabel(menuitem.GetBitmapBundle())

        # Yes both of the self.Layout() are necessary to do the sizing / wrap dance.
        self.Layout()
        w,_ = self.IncName.GetSize()
        self.IncName.Wrap(w)
        self.Layout()

    def BuildMenu(self, slot):
        menu = wx.Menu()

        incData = GameData.MiscPowers['Incarnate'][slot]

        for type in incData['Types']:
            submenu = wx.Menu()
            menu.AppendSubMenu(submenu, type)

            for index, power in enumerate(incData['Powers']):
                menuitem = wx.MenuItem(id = wx.ID_ANY, text = f"{type} {power}")
                rarity = Rarities[ index ]

                # aliases for the Lore types ie "Polar Lights" => "Lights" to match the icons
                aliasedtype = Aliases.get(type, type)


                iconname = f"Incarnate/Incarnate_{slot}_{aliasedtype}_{rarity}"
                icon = Icon(iconname)
                if icon: menuitem.SetBitmap(icon)

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
