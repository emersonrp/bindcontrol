from PowerBindCmd import PowerBindCmd
import wx

####### Target Custom
class TargetCustomCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        targetCustomSizer = wx.FlexGridSizer(2,3,3)
        targetCustomSizer.Add(wx.StaticText(dialog, -1, "Target Mode:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.RIGHT, 4)
        targetCustomModeChoice = wx.Choice(dialog, -1, choices = ['Near','Far','Next','Prev'])
        targetCustomModeChoice.SetSelection(0)
        targetCustomSizer.Add(targetCustomModeChoice)
        targetCustomSizer.Add(wx.CheckBox(dialog, -1, "Target Enemies"))
        targetCustomSizer.Add(wx.CheckBox(dialog, -1, "Target Friends"))
        targetCustomSizer.Add(wx.CheckBox(dialog, -1, "Target Defeated"))
        targetCustomSizer.Add(wx.CheckBox(dialog, -1, "Target Living"))
        targetCustomSizer.Add(wx.CheckBox(dialog, -1, "Target My Pets"))
        targetCustomSizer.Add(wx.CheckBox(dialog, -1, "Target Not My Pets"))
        targetCustomSizer.Add(wx.CheckBox(dialog, -1, "Target Base Items"))
        targetCustomSizer.Add(wx.CheckBox(dialog, -1, "Target Not Base Items"))

        return targetCustomSizer

