from PowerBindCmd import PowerBindCmd
import GameData
import wx


####### Use Insp By Name
class UseInspByNameCmd(PowerBindCmd):
    def BuildUI(self, dialog):
        useInspByNameSizer = wx.BoxSizer(wx.HORIZONTAL)
        useInspByNameSizer.Add(wx.StaticText(dialog, -1, "Inspiration:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        self.useInspByNameModeChoice = wx.Choice(dialog, -1, choices = self.GetAllInsps())
        self.useInspByNameModeChoice.SetSelection(0)
        useInspByNameSizer.Add(self.useInspByNameModeChoice, 1)

        return useInspByNameSizer

    def MakeBindString(self, dialog):
        choice = self.useInspByNameModeChoice
        index  = choice.GetSelection()
        mode   = choice.GetString(index)
        return "inspexecname " + mode.lower()


    def GetAllInsps(self):
        Insplist = []
        for type, info in GameData.Inspirations.items():
            for insp in info['tiers']:
                Insplist.append(insp)
        return sorted(Insplist)

