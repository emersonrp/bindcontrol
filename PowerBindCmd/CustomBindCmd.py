from PowerBindCmd import PowerBindCmd
import wx


####### Custom Bind
class CustomBindCmd(PowerBindCmd):
    def BuildUI(self, dialog):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.customBindName = wx.TextCtrl(dialog, -1)
        self.customBindName.SetHint('Custom Bind Text')
        sizer.Add(self.customBindName, 1, wx.ALIGN_CENTER_VERTICAL)

        return sizer

    def MakeBindString(self, dialog):
        return self.customBindName.GetValue()
