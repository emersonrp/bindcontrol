from PowerBindCmd import PowerBindCmd
import wx


####### Target Friend
class TargetFriendCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        targetFriendSizer = wx.BoxSizer(wx.HORIZONTAL)
        targetFriendSizer.Add(wx.StaticText(dialog, -1, "Target Friend:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        targetFriendModeChoice = wx.Choice(dialog, -1, choices = ['Near','Far','Next','Prev'])
        targetFriendModeChoice.SetSelection(0)
        targetFriendSizer.Add(targetFriendModeChoice)

        return targetFriendSizer

