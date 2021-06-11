from PowerBindCmd import PowerBindCmd
import wx


####### Away From Keyboard
class AFKCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        self.AFKName = wx.TextCtrl(dialog, -1)
        self.AFKName.SetHint('Away From Keyboard Text')

        return self.AFKName

    def MakeBindString(self):
        message = self.AFKName.GetValue()

        return f"afk {message}" if message else "afk"
