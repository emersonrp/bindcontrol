from PowerBindCmd import PowerBindCmd
import wx


####### Use Insp By Name
class UseInspByNameCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        useInspByNameSizer = wx.BoxSizer(wx.HORIZONTAL)
        useInspByNameSizer.Add(wx.StaticText(dialog, -1, "Inspiration:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        useInspByNameModeChoice = wx.Choice(dialog, -1, choices = self.GetAllInsps())
        useInspByNameModeChoice.SetSelection(0)
        useInspByNameSizer.Add(useInspByNameModeChoice, 1)

        return useInspByNameSizer

    def GetAllInsps(self):
        Insplist = []
        for type, info in GameData.Inspirations.items():
            for insp in info['tiers']:
                Insplist.append(insp)

        return sorted(Insplist)

