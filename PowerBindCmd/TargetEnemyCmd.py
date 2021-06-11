from PowerBindCmd import PowerBindCmd
import wx


####### Target Enemy
class TargetEnemyCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        targetEnemySizer = wx.BoxSizer(wx.HORIZONTAL)
        targetEnemySizer.Add(wx.StaticText(dialog, -1, "Target Enemy:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        targetEnemyModeChoice = wx.Choice(dialog, -1, choices = ['Near','Far','Next','Prev'])
        targetEnemyModeChoice.SetSelection(0)
        targetEnemySizer.Add(targetEnemyModeChoice)

        return targetEnemySizer

