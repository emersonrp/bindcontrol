from PowerBindCmd import PowerBindCmd
import wx


####### Custom Bind
class CustomBindCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        customBindName = wx.TextCtrl(dialog, -1)
        customBindName.SetHint('Custom Bind Text')

        return customBindName

