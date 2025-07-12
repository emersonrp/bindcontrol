import wx
import re
from Icon import GetIcon,GetIconBitmap
from Util.Incarnate import Rarities, Aliases

import GameData

class IncarnateBox(wx.StaticBoxSizer):
    def __init__(self, parent, server):
        wx.StaticBoxSizer.__init__(self, wx.HORIZONTAL, parent, 'Incarnate Powers')

        staticbox = self.GetStaticBox()
        self.Server = server

        incarnateSizer = wx.GridBagSizer(4, 4)

        self.Add(incarnateSizer, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 6)

        if self.Server == "Rebirth":
            self.genesisInc = IncarnatePicker(staticbox, label = "Genesis")

        self.hybridInc    = IncarnatePicker(staticbox, label = "Hybrid")
        self.loreInc      = IncarnatePicker(staticbox, label = "Lore")
        self.destinyInc   = IncarnatePicker(staticbox, label = "Destiny")
        self.judgementInc = IncarnatePicker(staticbox, label = "Judgement")
        self.interfaceInc = IncarnatePicker(staticbox, label = "Interface")
        self.alphaInc     = IncarnatePicker(staticbox, label = "Alpha")

        if self.Server == "Rebirth":
            incarnateSizer.Add(self.hybridInc,    wx.GBPosition(0,0), wx.GBSpan(1,2), wx.EXPAND|wx.LEFT, 12)
            incarnateSizer.Add(self.genesisInc,   wx.GBPosition(0,2), wx.GBSpan(1,2), wx.EXPAND|wx.RIGHT, 12)
        else:
            incarnateSizer.Add(self.hybridInc,    wx.GBPosition(0,1), wx.GBSpan(1,2), wx.EXPAND)

        incarnateSizer.Add(self.loreInc,      wx.GBPosition(1,0), wx.GBSpan(1,2), wx.EXPAND|wx.LEFT, 12)
        incarnateSizer.Add(self.destinyInc,   wx.GBPosition(1,2), wx.GBSpan(1,2), wx.EXPAND|wx.RIGHT, 12)
        incarnateSizer.Add(self.judgementInc, wx.GBPosition(2,0), wx.GBSpan(1,2), wx.EXPAND|wx.LEFT, 12)
        incarnateSizer.Add(self.interfaceInc, wx.GBPosition(2,2), wx.GBSpan(1,2), wx.EXPAND|wx.RIGHT, 12)
        incarnateSizer.Add(self.alphaInc,     wx.GBPosition(3,1), wx.GBSpan(1,2), wx.EXPAND|wx.BOTTOM, 12)

        incarnateSizer.AddGrowableCol(0)
        incarnateSizer.AddGrowableCol(1)
        incarnateSizer.AddGrowableCol(2)
        incarnateSizer.AddGrowableCol(3)

    def FillWith(self, incarnate):
        if incarnate:
            for boxname, contents in incarnate.items():
                box = getattr(self, boxname.lower() + "Inc", None)
                if box:
                    box.IncName.SetLabel(contents['power'])
                    box.IncIcon.SetBitmapLabel(GetIconBitmap(contents['iconfile']))
                    box.IconFilename = contents['iconfile']

    def GetData(self):
        incarnatedata = {}

        boxes = [self.hybridInc, self.loreInc, self.destinyInc, self.judgementInc, self.interfaceInc, self.alphaInc]
        if self.Server == "Rebirth":
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
    def __init__(self, parent, label = ""):
        wx.StaticBoxSizer.__init__(self, wx.HORIZONTAL, parent, label = label)
        staticbox = self.GetStaticBox()

        self.Label = label
        self.IconFilename = ''
        self.PopupMenu = None

        hsizer = wx.BoxSizer(wx.HORIZONTAL)

        # "Themed" GenBitmapButton looks flat etc the way we want it to.
        self.IncIcon = buttons.ThemedGenBitmapButton(staticbox, bitmap = GetIconBitmap('Empty'), size=wx.Size(39,40))
        setattr(self.IncIcon, 'Picker', self)
        self.IncIcon.Bind(wx.EVT_BUTTON, self.OnButtonPress)
        self.IncIcon.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)
        self.IncName = wx.StaticText(staticbox, wx.ID_ANY, style=wx.ALIGN_RIGHT, size=wx.Size(310, -1))

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

        # Yes both of the self.Layout() are necessary to do the sizing / wrap dance.
        self.Layout()
        w,_ = self.IncName.GetSize()
        self.IncName.Wrap(w)
        self.Layout()
        evt.Skip()

    def OnRightClick(self, evt):
        button = evt.EventObject
        button.SetBitmapLabel(GetIconBitmap('Empty'))
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

                icon = GetIcon('Incarnate', f'Incarnate_{slot}_{aliasedtype}_{rarity}')
                if icon: menuitem.SetBitmap(icon)
                setattr(menuitem, 'IconFilename', icon.Filename)

                submenu.Append(menuitem)

        menuitem = wx.MenuItem(id = wx.ID_ANY, text = "Disable Slot")
        icon = GetIcon('Incarnate', 'Disable')
        if icon: menuitem.SetBitmap(icon)
        setattr(menuitem, 'IconFilename', icon.Filename)

        menu.Append(menuitem)

        return menu
