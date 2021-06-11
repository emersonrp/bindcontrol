from PowerBindCmd import PowerBindCmd
import wx


####### Window Toggle
class WindowToggleCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        windows = [ 'Actions', 'Badge', 'ChanSearch', 'Chat', 'Chat0', 'Chat1', 'Chat2', 'Chat3',
            'Chat4', 'Clue', 'Combatmonitor', 'Combatnumbers', 'Compass', 'Compose', 'Contact',
            'Costume', 'Email', 'Enhancements', 'Friend', 'Group', 'Help', 'Info', 'Inspirations',
            'Map', 'Mission', 'Nav', 'Options', 'Pet', 'Power', 'PowerList', 'Recipes', 'Salvage',
            'Search', 'Supergroup', 'Team', 'Target', 'Tray', ]
        windowToggleSizer = wx.BoxSizer(wx.HORIZONTAL)
        windowToggleSizer.Add(wx.StaticText(dialog, -1, "Window:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        self.windowToggleTray = wx.Choice(dialog, -1, choices = windows)
        self.windowToggleTray.SetSelection(0)
        windowToggleSizer.Add(self.windowToggleTray, 1, wx.ALIGN_CENTER_VERTICAL)

        return windowToggleSizer

    def MakeBindString(self, dialog):
        choice = self.windowToggleTray
        index  = choice.GetSelection()
        window = choice.GetString(index)
        return "windowtoggle " + lower(window)

