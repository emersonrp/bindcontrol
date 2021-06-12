from PowerBindCmd import PowerBindCmd
import wx

####### Auto Power
class AutoPowerCmd(PowerBindCmd):
    def BuildUI(self, dialog):
        autoPowerSizer = wx.BoxSizer(wx.HORIZONTAL)
        autoPowerSizer.Add(wx.StaticText(dialog, -1, "Power:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        self.autoPowerName = wx.TextCtrl(dialog, -1)
        autoPowerSizer.Add(self.autoPowerName, 1, wx.ALIGN_CENTER_VERTICAL)

        return autoPowerSizer

    def MakeBindString(self, dialog):
        return f"powexecauto {self.autoPowerName.GetValue()}"

