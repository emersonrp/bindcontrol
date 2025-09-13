import wx
import re
from wx.adv import BitmapComboBox
import GameData
from Icon import GetIconBitmap
from UI.PowerBinderCommand import PowerBinderCommand

####### Use Insp By Name
class InspCombine(PowerBinderCommand):
    Name = "Combine Inspirations"
    Menu = "Inspirations"

    def BuildUI(self, dialog):
        inspCombineSizer = wx.FlexGridSizer(2, 2, 5)

        inspCombineSizer.Add(wx.StaticText(dialog, -1, "Combine 3:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.RIGHT, 4)
        self.inspCombineSource = BitmapComboBox(dialog, style = wx.CB_READONLY)
        self.inspCombineSource.SetMinSize(wx.Size(350,-1))
        for _, types in GameData.Inspirations.items():
            for _, info in types.items():
                for insp in info['tiers']:
                    name = re.sub(' ', '', str(insp))
                    icon = GetIconBitmap(f'Inspirations', name)
                    self.inspCombineSource.Append(insp, icon)
        self.inspCombineSource.SetSelection(0)
        inspCombineSizer.Add(self.inspCombineSource, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)

        inspCombineSizer.Add(wx.StaticText(dialog, -1, "Into 1:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.RIGHT, 4)
        self.inspCombineTarget = BitmapComboBox(dialog, style = wx.CB_READONLY)
        self.inspCombineTarget.SetMinSize(wx.Size(350,-1))
        for _, types in GameData.Inspirations.items():
            for _, info in types.items():
                for insp in info['tiers']:
                    name = re.sub(' ', '', str(insp))
                    icon = GetIconBitmap(f'Inspirations', name)
                    self.inspCombineTarget.Append(insp, icon)
        self.inspCombineTarget.SetSelection(0)
        inspCombineSizer.Add(self.inspCombineTarget, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)

        return inspCombineSizer

    def MakeBindString(self):
        schoice = self.inspCombineSource
        sindex  = schoice.GetSelection()
        source  = re.sub(' ', '_', schoice.GetString(sindex))
        tchoice = self.inspCombineTarget
        tindex  = tchoice.GetSelection()
        target  = re.sub(' ', '_', tchoice.GetString(tindex))
        cmd = "mergeinsp" if self.Profile.Server() == "Homecoming" else "inspcombine"
        return f'{cmd} {source.lower()} {target.lower()}'

    def GetAllInsps(self):
        Insplist = []
        for _, info in GameData.Inspirations.items():
            for insp in info['tiers']:
                Insplist.append(insp)
            Insplist.append("---")
        Insplist.pop(-1) # snip the terminal "---"

        return Insplist

    def Serialize(self):
        schoice = self.inspCombineSource
        sindex  = schoice.GetSelection()
        source  = schoice.GetString(sindex)
        tchoice = self.inspCombineTarget
        tindex  = tchoice.GetSelection()
        target  = tchoice.GetString(tindex)
        return {
                'source' : source,
                'target' : target,
                }

    def Deserialize(self, init):
        if source := init.get('source', ''):
            self.inspCombineSource.SetSelection(self.inspCombineSource.FindString(source))
        if target := init.get('target', ''):
            self.inspCombineTarget.SetSelection(self.inspCombineTarget.FindString(target))
