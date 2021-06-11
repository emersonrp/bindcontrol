from PowerBindCmd import PowerBindCmd
import wx


####### Window Toggle
class WindowToggleCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        windowToggleSizer = wx.BoxSizer(wx.HORIZONTAL)
        windowToggleSizer.Add(wx.StaticText(dialog, -1, "Tray:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        windowToggleTray = wx.Choice(dialog, -1,
               choices = ['Powers', 'Manage', 'Chat', 'Tray', 'Target', 'Nav', 'Map', 'Menu', 'Pets'])
        windowToggleTray.SetSelection(0)
        windowToggleSizer.Add(windowToggleTray, 1, wx.ALIGN_CENTER_VERTICAL)

        return windowToggleSizer


