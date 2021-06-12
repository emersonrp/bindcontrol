from PowerBindCmd import PowerBindCmd
import wx


####### Away From Keyboard
class AFKCmd(PowerBindCmd):
    def BuildUI(self, dialog):
        self.AFKName = wx.TextCtrl(dialog, -1)
        self.AFKName.SetHint('Away From Keyboard Text')

        return self.AFKName

    def MakeBindString(self, dialog):
        message = self.AFKName.GetValue()

        return f"afk {message}" if message else "afk"
