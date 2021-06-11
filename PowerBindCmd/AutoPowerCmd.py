from PowerBindCmd import PowerBindCmd
import wx

####### Auto Power
class AutoPowerCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        autoPowerSizer = wx.BoxSizer(wx.HORIZONTAL)
        autoPowerSizer.Add(wx.StaticText(dialog, -1, "Power:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        autoPowerName = wx.TextCtrl(dialog, -1)
        autoPowerSizer.Add(autoPowerName, 1, wx.ALIGN_CENTER_VERTICAL)

        return autoPowerSizer

    def Make(self, dialog):
        pass

