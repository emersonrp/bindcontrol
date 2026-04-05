import wx
from pubsub import pub
import re
from wx.adv import BitmapComboBox
import GameData
from Icon import GetIconBitmap
from UI.PowerBinderCommand import PowerBinderCommand

####### Use Insp By Name
class UseInspByNameCmd(PowerBinderCommand):
    Name = "Use Inspiration By Name"
    Menu = "Inspirations"
    DeprecatedName = "Use Insp By Name"

    def BuildUI(self, dialog) -> wx.BoxSizer:
        useInspByNameSizer = wx.BoxSizer(wx.HORIZONTAL)
        useInspByNameSizer.Add(wx.StaticText(dialog, label = "Inspiration:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        self.useInspByNameModeChoice = BitmapComboBox(dialog, style = wx.CB_READONLY)
        for _, types in GameData.Inspirations.items():
            for _, info in types.items():
                for insp in info['tiers']:
                    name = re.sub(' ', '', str(insp))
                    icon = GetIconBitmap('Inspirations', name)
                    self.useInspByNameModeChoice.Append(insp, icon)
        self.useInspByNameModeChoice.SetSelection(0)
        useInspByNameSizer.Add(self.useInspByNameModeChoice, 1, wx.ALIGN_CENTER_VERTICAL)

        return useInspByNameSizer

    def MakeBindString(self) -> str:
        return "inspexecname " + self.useInspByNameModeChoice.GetStringSelection().lower()

    def GetAllInsps(self) -> list:
        Insplist = []
        for _, info in GameData.Inspirations.items():
            for insp in info['tiers']:
                Insplist.append(insp)
            Insplist.append("---")
        Insplist.pop(-1) # snip the terminal "---"

        return Insplist

    def Serialize(self) -> dict:
        return { 'insp' : self.useInspByNameModeChoice.GetStringSelection() }

    def Deserialize(self, init) -> None:
        insp = init.get('insp', 0)
        if isinstance(insp, int):
            self.useInspByNameModeChoice.SetSelection(insp)
            # If we touch one that is int-based, mark it as needing re-saving.
            # TODO:  is there a trivial way to tell it "resave the whole thing,
            # examining and updating all steps?"  Probably not.
            pub.sendMessage('updatebinds')
        elif isinstance(insp, str):
            self.useInspByNameModeChoice.SetStringSelection(insp)
