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

    def BuildUI(self, dialog) -> wx.FlexGridSizer:
        inspCombineSizer = wx.FlexGridSizer(2, 2, 5)

        inspCombineSizer.Add(wx.StaticText(dialog, label = "Combine 3:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.RIGHT, 4)
        self.inspCombineSource = BitmapComboBox(dialog, style = wx.CB_READONLY)
        self.inspCombineSource.SetMinSize(wx.Size(350,-1))
        for info in GameData.Inspirations['Single'].values():
            for insp in info['tiers'][0:3]:
                name = re.sub(' ', '', str(insp))
                icon = GetIconBitmap('Inspirations', name)
                self.inspCombineSource.Append(insp, icon)
        self.inspCombineSource.SetSelection(0)
        self.inspCombineSource.Bind(wx.EVT_COMBOBOX, self.OnSourceSelect)
        inspCombineSizer.Add(self.inspCombineSource, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)

        inspCombineSizer.Add(wx.StaticText(dialog, label = "Into 1:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.RIGHT, 4)
        self.inspCombineTarget = BitmapComboBox(dialog, style = wx.CB_READONLY)
        self.inspCombineTarget.SetMinSize(wx.Size(350,-1))
        for info in GameData.Inspirations['Single'].values():
            for insp in info['tiers'][0:3]:
                name = re.sub(' ', '', str(insp))
                icon = GetIconBitmap('Inspirations', name)
                self.inspCombineTarget.Append(insp, icon)
        self.inspCombineTarget.SetSelection(0)
        inspCombineSizer.Add(self.inspCombineTarget, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)

        self.OnSourceSelect()

        return inspCombineSizer

    def OnSourceSelect(self, evt = None):
        sourceidx  = self.inspCombineSource.GetSelection()
        sourcename = self.inspCombineSource.GetStringSelection()
        currtarget = self.inspCombineTarget.GetStringSelection()

        # Decide which 'power' it is, wee, medium, large, super
        power = sourceidx % 3
        targetlist = []
        # build list of the same power
        for info in GameData.Inspirations['Single'].values():
            tierinsp = info['tiers'][power]
            # don't convert to yourself
            if tierinsp == sourcename: continue
            targetlist.append(tierinsp)

        # Fill out the target picker with the rest of the insps of the same power
        self.inspCombineTarget.Clear()
        for insp in targetlist:
            name = re.sub(' ', '', str(insp))
            icon = GetIconBitmap('Inspirations', name)
            self.inspCombineTarget.Append(insp, icon)

        # If we had already picked that one but just changed our source to the same power,
        # keep the existing target.  If not, just pick the first one.
        if self.inspCombineTarget.FindString(currtarget):
            self.inspCombineTarget.SetStringSelection(currtarget)
        else:
            self.inspCombineTarget.SetSelection(0)

        if evt: evt.Skip()

    def MakeBindString(self) -> str:
        source  = re.sub(' ', '_', self.inspCombineSource.GetStringSelection())
        target  = re.sub(' ', '_', self.inspCombineTarget.GetStringSelection())
        cmd = "mergeinsp" if self.Profile.Server() == "Homecoming" else "inspcombine"
        return f'{cmd} {source.lower()} {target.lower()}'

    def Serialize(self) -> dict:
        return {
                'source' : self.inspCombineSource.GetStringSelection(),
                'target' : self.inspCombineTarget.GetStringSelection(),
                }

    def Deserialize(self, init) -> None:
        if source := init.get('source', ''):
            self.inspCombineSource.SetStringSelection(source)
        self.OnSourceSelect()
        if target := init.get('target', ''):
            self.inspCombineTarget.SetStringSelection(target)
