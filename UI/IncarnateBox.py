from typing import Dict, Any
import wx
import wx.html
import wx.lib.mixins.listctrl as listmix

import re
from Icon import GetIcon,GetIconBitmap
from Util.Incarnate import Rarities, Aliases, SlotData

class IncarnateBox(wx.StaticBoxSizer):
    def __init__(self, parent, server) -> None:
        super().__init__(wx.HORIZONTAL, parent, 'Incarnate Powers')

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

    def FillWith(self, incarnate) -> None:
        if incarnate:
            for boxname, contents in incarnate.items():
                box = getattr(self, boxname.lower() + "Inc", None)
                if box:
                    box.IncName.SetLabel(contents['power'])
                    box.IncIcon.SetBitmapLabel(GetIconBitmap(contents['iconfile']))
                    box.IconFilename = contents['iconfile']

    def Serialize(self) -> Dict[str, str]:
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
    def __init__(self, parent, slot = "") -> None:
        super().__init__(wx.HORIZONTAL, parent, label = slot)
        staticbox = self.GetStaticBox()

        self.Slot = slot
        self.IconFilename = ''
        self.SlotData = SlotData[slot]

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

    def OnButtonPress(self, evt) -> None:
        with IncarnateBrowser(self) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                if powerdata := dlg.GetPickedPower():

                    self.IncName.SetLabel(powerdata['PowerName'])
                    self.IncIcon.SetBitmapLabel(powerdata['Icon'])
                    self.IconFilename = powerdata['IconFilename']

                    # Yes both of the self.Layout() are necessary to do the sizing / wrap dance.
                    self.Layout()
                    w,_ = self.IncName.GetSize()
                    self.IncName.Wrap(w)
                    self.Layout()

        evt.Skip()

    def OnRightClick(self, evt) -> None:
        button = evt.EventObject
        button.SetBitmapLabel(GetIconBitmap('Empty'))
        button.Picker.IncName.SetLabel('')
        button.Layout()
        evt.Skip()

class IncarnateBrowserList(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID = -1, pos = wx.DefaultPosition,
                 size = wx.Size(250, -1), style = wx.LC_REPORT|wx.LC_NO_HEADER|wx.LC_SINGLE_SEL) -> None:
        super().__init__(parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)

        self.IconFilenames = []

class IncarnateBrowser(wx.Dialog):
    def __init__(self, picker) -> None:
        super().__init__(None, title = f"{picker.Slot} slot")
        self.Picker = picker

        boxsize = wx.Size(400, 300)
        browserSizer = wx.BoxSizer(wx.VERTICAL)

        listSizer = wx.GridSizer(3)

        self.TypeList = IncarnateBrowserList(self, size = boxsize)
        self.TypeList.AppendColumn('')
        self.TypeList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onPickType)
        typeImgList = wx.ImageList(32,32)
        self.TypeList.AssignImageList(typeImgList, wx.IMAGE_LIST_SMALL)

        for i, type in enumerate(list(picker.SlotData)):
            slot = self.Picker.Slot
            aliasedtype = Aliases.get(type, type)
            typeImgList.Add(GetIconBitmap('Incarnate', f'Incarnate_{slot}_{aliasedtype}_VeryRare'))
            self.TypeList.InsertItem(self.TypeList.GetItemCount(), type, i)
        nextentry = len(picker.SlotData)
        typeImgList.Add(GetIconBitmap('Incarnate', 'Disable'))
        self.TypeList.InsertItem(nextentry, "Disable Slot", nextentry)
        listSizer.Add(self.TypeList, 1, wx.EXPAND)

        self.LevelList = IncarnateBrowserList(self, size = boxsize)
        self.LevelList.AppendColumn('')
        self.LevelList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onPickLevel)
        listSizer.Add(self.LevelList, 1, wx.EXPAND)

        self.IncDetails = wx.html.HtmlWindow(self, size = boxsize)
        listSizer.Add(self.IncDetails, 1, wx.EXPAND)

        browserSizer.Add(listSizer, 1, wx.EXPAND|wx.ALL, 10)

        buttonSizer = self.CreateButtonSizer(wx.OK|wx.CANCEL)
        browserSizer.Add(buttonSizer, 0, wx.EXPAND|wx.ALL, 10)

        self.SetSizerAndFit(browserSizer)
        self.Layout()

    def GetPickedPower(self) -> Dict[str, Any]:
        # First, check if we've decided on 'Disable'
        typeidx = self.TypeList.GetFirstSelected()
        typeitem = self.TypeList.GetItem(typeidx)
        if typeitem.GetText() == "Disable Slot":
            iconlist = self.TypeList.GetImageList(wx.IMAGE_LIST_SMALL)
            icon = iconlist.GetBitmap(typeitem.GetImage())

            return {
                'PowerName'    : 'Disable Slot',
                'Icon'         : icon,
                'IconFilename' : GetIcon('Incarnate', 'Disable').Filename,
            }

        pickedidx = self.LevelList.GetFirstSelected()
        if pickedidx == -1:
            return {}
        pickeditem = self.LevelList.GetItem(pickedidx)
        iconlist = self.LevelList.GetImageList(wx.IMAGE_LIST_SMALL)
        icon = iconlist.GetBitmap(pickeditem.GetImage())

        return {
            'PowerName'    : pickeditem.GetText(),
            'Icon'         : icon,
            'IconFilename' : self.LevelList.IconFilenames[pickedidx],
        }

    def onPickType(self, evt) -> None:
        self.LevelList.DeleteAllItems()
        self.IncDetails.SetPage('')

        type = self.TypeList.GetItemText(evt.GetIndex())

        if type == 'Disable Slot': return

        lvlImgList = wx.ImageList(32,32)
        self.LevelList.AssignImageList(lvlImgList, wx.IMAGE_LIST_SMALL)

        for i, level in enumerate(list(self.Picker.SlotData[type])):
            rarity = Rarities[i]
            slot = self.Picker.Slot
            aliasedtype = Aliases.get(type, type)
            icon = GetIcon('Incarnate', f'Incarnate_{slot}_{aliasedtype}_{rarity}')
            lvlImgList.Add(icon.GetBitmap(wx.Size(32,32)))
            self.LevelList.IconFilenames.append(icon.Filename)
            self.LevelList.InsertItem(self.LevelList.GetItemCount(), level, i)

    def onPickLevel(self, evt):
        type = self.TypeList.GetItemText(self.TypeList.GetFirstSelected())
        level = self.LevelList.GetItemText(evt.GetIndex())
        info = self.Picker.SlotData[type][level]

        self.IncDetails.SetPage(info)
