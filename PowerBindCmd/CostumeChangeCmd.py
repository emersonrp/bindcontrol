from PowerBindCmd import PowerBindCmd
import wx

#######Costume Change
class CostumeChangeCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        costumeChangeSizer = wx.BoxSizer(wx.HORIZONTAL)
        costumeChangeSizer.Add(wx.StaticText(dialog, -1, "Costume:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        costumeChangeCostume = wx.Choice(dialog, -1,
               choices = ["First", "Second", "Third", "Fourth", "Fifth"])
        costumeChangeCostume.SetSelection(0)
        costumeChangeSizer.Add(costumeChangeCostume, 1, wx.ALIGN_CENTER_VERTICAL)

        return costumeChangeSizer


