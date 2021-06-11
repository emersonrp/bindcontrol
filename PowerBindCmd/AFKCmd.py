from PowerBindCmd import PowerBindCmd
import wx


####### Away From Keyboard
class AFKCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        AFKIndex = self.bindChoice.FindString("Away From Keyboard")
        AFKName = wx.TextCtrl(self, -1)
        AFKName.SetHint('Away From Keyboard Text')

        return AFKName

