from PowerBindCmd import PowerBindCmd
import wx


####### Away From Keyboard
class AFKCmd(PowerBindCmd):
    def BuildUI(self, dialog):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.AFKName = wx.TextCtrl(dialog, -1)
        self.AFKName.SetHint('Away From Keyboard Text')
        sizer.Add(self.AFKName, 1, wx.ALIGN_CENTER_VERTICAL)

        return sizer

    def MakeBindString(self, dialog):
        message = self.AFKName.GetValue()

        return f"afk {message}" if message else "afk"
