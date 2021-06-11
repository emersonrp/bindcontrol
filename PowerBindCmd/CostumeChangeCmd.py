from PowerBindCmd import PowerBindCmd
import wx

#######Costume Change
class CostumeChangeCmd(PowerBindCmd):
    def BuildUI(self, dialog):
        costumeChangeSizer = wx.BoxSizer(wx.HORIZONTAL)
        costumeChangeSizer.Add(wx.StaticText(dialog, -1, "Costume:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        self.costumeChangeCostume = wx.Choice(dialog, -1,
               choices = ["First", "Second", "Third", "Fourth", "Fifth"])
        self.costumeChangeCostume.SetSelection(0)
        costumeChangeSizer.Add(self.costumeChangeCostume, 1, wx.ALIGN_CENTER_VERTICAL)

        return costumeChangeSizer

    def MakeBindString(self, dialog):
        costumeNumber = self.costumeChangeCostume.GetSelection() + 1

        return f"cc {costumeNumber}"
