import wx
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

    def BuildUI(self, dialog):
        useInspByNameSizer = wx.BoxSizer(wx.HORIZONTAL)
        useInspByNameSizer.Add(wx.StaticText(dialog, -1, "Inspiration:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        self.useInspByNameModeChoice = BitmapComboBox(dialog, style = wx.CB_READONLY)
        for _, types in GameData.Inspirations.items():
            for _, info in types.items():
                for insp in info['tiers']:
                    name = re.sub(' ', '', str(insp))
                    icon = GetIconBitmap(f'Inspirations', name)
                    self.useInspByNameModeChoice.Append(insp, icon)
        self.useInspByNameModeChoice.SetSelection(0)
        useInspByNameSizer.Add(self.useInspByNameModeChoice, 1, wx.ALIGN_CENTER_VERTICAL)

        return useInspByNameSizer

    def MakeBindString(self):
        choice = self.useInspByNameModeChoice
        index  = choice.GetSelection()
        mode   = choice.GetString(index)
        return "inspexecname " + mode.lower()

    def GetAllInsps(self):
        Insplist = []
        for _, info in GameData.Inspirations.items():
            for insp in info['tiers']:
                Insplist.append(insp)
            Insplist.append("---")
        Insplist.pop(-1) # snip the terminal "---"

        return Insplist

    # TODO - we're serializing GetSelection() which could, in principle, change
    # if the game changes up the inspirations.  We should dtrt with storing the
    # string instead, and still honoring isinstance(int) to support legacy profiles

    def Serialize(self):
        return { 'insp' : self.useInspByNameModeChoice.GetSelection() }

    def Deserialize(self, init):
        if init.get('insp', ''): self.useInspByNameModeChoice.SetSelection(init['insp'])
