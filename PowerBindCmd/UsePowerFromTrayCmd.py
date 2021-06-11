from PowerBindCmd import PowerBindCmd
import wx


####### Use Power From Tray
class UsePowerFromTrayCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        usePowerFromTraySizer = wx.BoxSizer(wx.HORIZONTAL)
        usePowerFromTraySizer.Add(wx.StaticText(dialog, -1, "Tray:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        usePowerFromTrayTray = wx.Choice(dialog, -1,
               choices = ['Main Tray', 'Alt Tray', 'Alt 2 Tray', 'Tray 1', 'Tray2', 'Tray 3',
                   'Tray 4', 'Tray 5', 'Tray 6', 'Tray 7', 'Tray 8', 'Tray 9', 'Tray 10'])
        usePowerFromTrayTray.SetSelection(0)
        usePowerFromTraySizer.Add(usePowerFromTrayTray, 1, wx.ALIGN_CENTER_VERTICAL)
        usePowerFromTraySizer.Add(wx.StaticText(dialog, -1, "Slot:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        usePowerFromTraySlot = wx.SpinCtrl(dialog, -1, style=wx.SP_ARROW_KEYS)
        usePowerFromTraySlot.SetRange(1, 10)
        usePowerFromTraySizer.Add(usePowerFromTraySlot, 1, wx.ALIGN_CENTER_VERTICAL)

        return usePowerFromTraySizer

