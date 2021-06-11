from PowerBindCmd import PowerBindCmd
import wx


####### Use Power
class UsePowerCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        usePowerSizer = wx.GridBagSizer(5,5)
        usePowerSizer.Add(wx.StaticText(dialog, -1, "Method:"), (0,0), flag=wx.ALIGN_CENTER_VERTICAL)
        usePowerSizer.Add(wx.RadioButton(dialog, -1, "Toggle", style=wx.RB_GROUP|wx.ALIGN_CENTER_VERTICAL), (0,1))
        usePowerSizer.Add(wx.RadioButton(dialog, -1, "On", style=wx.ALIGN_CENTER_VERTICAL), (0,2))
        usePowerSizer.Add(wx.RadioButton(dialog, -1, "Off", style=wx.ALIGN_CENTER_VERTICAL), (0,3))
        usePowerSizer.Add(wx.StaticText(dialog, -1, "Power:"), (1,0), flag=wx.ALIGN_CENTER_VERTICAL)
        usePowerName = wx.TextCtrl(dialog, -1)
        usePowerName.SetHint('Power Name')
        usePowerSizer.Add(usePowerName, (1,1), (1,3), flag=wx.EXPAND)
        usePowerSizer.AddGrowableCol(3)

        return usePowerSizer

