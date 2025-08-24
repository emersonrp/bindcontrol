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
            self.genesisInc = IncarnatePicker(staticbox, slot = "Genesis")

        self.hybridInc    = IncarnatePicker(staticbox, slot = "Hybrid")
        self.loreInc      = IncarnatePicker(staticbox, slot = "Lore")
        self.destinyInc   = IncarnatePicker(staticbox, slot = "Destiny")
        self.judgementInc = IncarnatePicker(staticbox, slot = "Judgement")
        self.interfaceInc = IncarnatePicker(staticbox, slot = "Interface")
        self.alphaInc     = IncarnatePicker(staticbox, slot = "Alpha")

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

    def Serialize(self):
        incarnatedata = {}

        boxes = [self.hybridInc, self.loreInc, self.destinyInc, self.judgementInc, self.interfaceInc, self.alphaInc]
        if self.Server == "Rebirth":
            boxes.append(self.genesisInc)

        for box in boxes:
            if box.IncName.GetLabel():
                incarnatedata[box.Slot] = {
                    'power'    : re.sub('\n', ' ', box.IncName.GetLabel()),
                    'iconfile' : box.IconFilename,
                }
        return incarnatedata

import wx.lib.buttons as buttons
class IncarnatePicker(wx.StaticBoxSizer):
    def __init__(self, parent, slot = ""):
        wx.StaticBoxSizer.__init__(self, wx.HORIZONTAL, parent, label = slot)
        staticbox = self.GetStaticBox()

        self.Slot = slot
        self.IconFilename = ''
        self.SlotData = self.BuildSlotData()

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

    def OnButtonPress(self, _):
        # TODO "if showmodal == OK etc etc"
        with IncarnateBrowser(self) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                print("Gonna Do The Thing")

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

    def BuildSlotData(self):

        if self.Slot == 'Lore': return self.BuildLoreSlotData()

        rawdata = GameData.IncarnatePowers[self.Slot]

        slotdata = {}

        for typename, typedata in rawdata['Types'].items():
            slotdata[typename] = {}
            for i, levelname in enumerate(rawdata['Levels']):
                effecttext = ''
                for j, effectname in enumerate(typedata['Effects']):
                    effectdata = typedata['Levels'][i][j]
                    if isinstance(effectdata, int) and effectdata == 0:
                        continue
                    if isinstance(effectdata, list):
                        effectline = "\n".join(effectdata)
                    elif isinstance(effectdata, str):
                        effectline = f"{effectdata}\n"
                    elif isinstance(effectdata, int) and effectdata == 1:
                        effectline = f"{effectname}\n"
                    else:
                        raise Exception(f'Something is terribly wrong with the incarnate data at {typename}, {i}, {j}: {effectdata}')
                    effecttext = effecttext + f"{effectname}: {effectline}"

                slotdata[typename][f'{typename} {levelname}'] = effecttext

        return slotdata

    def BuildLoreSlotData(self):

        rawdata = GameData.IncarnatePowers['Lore']

        slotdata = {}

        for typename, typedata in rawdata['Types'].items():
            slotdata[typename] = {}
            for leveldata in rawdata['Levels']:
                effecttext = ''
                (levelname, min, lt, bos, special, lvlshift) = leveldata

                if min: effecttext = effecttext + f"Summon {typedata[0]}\n"
                if lt : effecttext = effecttext + f"Summon {typedata[1]}\n"
                if bos: effecttext = effecttext + f"Summon {typedata[2]}\n"
                if special:
                    if special == "+DMG":
                        effecttext = effecttext + f"{special}\n"
                    else:
                        effecttext = effecttext + f"{typedata[2]} {special}\n"
                if lvlshift: effecttext = effecttext + "Incarnate Level Shift\n"

                slotdata[typename][f'{typename} {levelname}'] = effecttext

        return slotdata

class IncarnateBrowser(wx.Dialog):
    def __init__(self, picker):
        super().__init__(None, title = f"{picker.Slot} slot")
        self.Picker = picker

        browserSizer = wx.BoxSizer(wx.VERTICAL)

        listSizer = wx.GridSizer(3)

        self.TypeList = wx.ListCtrl(self, style = wx.LC_REPORT|wx.LC_NO_HEADER|wx.LC_SINGLE_SEL)
        self.TypeList.AppendColumn('')
        self.TypeList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onPickType)
        for type in list(picker.SlotData):
            self.TypeList.Append([type])
        listSizer.Add(self.TypeList, 1, wx.EXPAND)

        self.LevelList = wx.ListCtrl(self, style = wx.LC_REPORT|wx.LC_NO_HEADER|wx.LC_SINGLE_SEL)
        self.LevelList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onPickLevel)
        listSizer.Add(self.LevelList, 1, wx.EXPAND)

        self.IncDetails = wx.StaticText(self, style = wx.ST_NO_AUTORESIZE)
        listSizer.Add(self.IncDetails, 1, wx.EXPAND)

        browserSizer.Add(listSizer, 1, wx.EXPAND|wx.ALL, 10)

        buttonSizer = self.CreateButtonSizer(wx.OK|wx.CANCEL)
        browserSizer.Add(buttonSizer, 0, wx.EXPAND|wx.ALL, 10)

        self.SetSizerAndFit(browserSizer)
        self.Layout()

    def PickedPower(self):
        ...

    def onPickType(self, evt):
        self.LevelList.ClearAll()
        self.LevelList.AppendColumn('')
        type = self.TypeList.GetItemText(evt.GetIndex())
        for level in list(self.Picker.SlotData[type]):
            self.LevelList.Append([level])

    def onPickLevel(self, evt):
        type = self.TypeList.GetItemText(self.TypeList.GetFirstSelected())
        level = self.LevelList.GetItemText(evt.GetIndex())
        info = self.Picker.SlotData[type][level]

        self.IncDetails.SetLabel(info)

