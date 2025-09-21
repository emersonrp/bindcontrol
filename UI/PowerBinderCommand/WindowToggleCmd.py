import wx
from UI.PowerBinderCommand import PowerBinderCommand

####### Window Toggle
class WindowToggleCmd(PowerBinderCommand):
    Name = "Window Toggle"
    Menu = "Graphics / UI"

    def BuildUI(self, dialog) -> wx.BoxSizer:
        # Having a window name of '' means you can't open/close/toggle because there's a special command
        self.WindowNames = {
                'Actions'             : 'actions',
                'Arena List'          : '',
                'Auction House'       : 'ah',
                'Badge'               : 'badge',
                'Channel Search'      : 'chansearch',
                'Chat'                : 'chat',
                'Custom Chat 1'       : 'chat1',
                'Custom Chat 2'       : 'chat2',
                'Custom Chat 3'       : 'chat3',
                'Custom Chat 4'       : 'chat4',
                'Clues'               : 'clue',
                'Combat Numbers'      : 'combatnumbers',
                'Contacts'            : 'contact',
                'Contact Finder'      : 'contactfinder',
                'Costumes'            : 'costume',
                'Email'               : 'email',
                'Enhancements'        : 'enhancements',
                'Friends'             : 'friend',
                'Group'               : 'group',
                'Help'                : 'helpwindow',
                'Incarnate'           : 'incarnate',
                'Inspirations'        : 'insp',
                'League'              : 'league',
                'LFG'                 : 'lfg',
                'Manage Enhancements' : '',
                'Map'                 : 'map',
                'Mission'             : 'mission',
                'Nav / Compass'       : 'nav',
                'Options'             : 'options',
                'Pets'                : 'pet',
                'Petition'            : 'petition',
                'Power Tray'          : 'powers',
                'Power List'          : 'powerlist',
                'Quit'                : 'quit',
                'Recipes'             : 'recipe',
                'Salvage'             : 'salvage',
                'Search'              : 'search',
                'Supergroup'          : 'sg',
                'Target'              : 'target',
                'Team'                : 'team',
                'Tray'                : 'tray',
                'Tray1'               : 'tray1',
                'Tray2'               : 'tray2',
                'Tray3'               : 'tray3',
                'Tray4'               : 'tray4',
                'Tray5'               : 'tray5',
                'Tray6'               : 'tray6',
                'Tray7'               : 'tray7',
                'Tray8'               : 'tray8',
                'Vault'               : 'vault',
            }

        self.ShortToggleCommands = {
                'Arena List'          : 'arenalist',
                'Auction House'       : 'ah',
                'Chat'                : 'chat',
                'Help'                : 'helpwindow',
                'Map'                 : 'map',
                'Manage Enhancements' : 'manage',
                'Nav / Compass'       : 'nav',
                'Power Tray'          : 'powers',
                'Target'              : 'target',
                'Tray'                : 'tray',
            }

        windowToggleSizer = wx.BoxSizer(wx.HORIZONTAL)
        windowToggleSizer.Add(wx.StaticText(dialog, -1, "Window:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        self.windowToggleTray = wx.Choice(dialog, -1, choices = list(self.WindowNames.keys()))
        self.windowToggleTray.SetSelection(0)
        self.windowToggleTray.Bind(wx.EVT_CHOICE, self.OnWindowPicked)
        windowToggleSizer.Add(self.windowToggleTray, 1, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)

        self.windowToggleRB = wx.RadioButton(dialog, -1, "Toggle", style = wx.RB_GROUP)
        self.windowShowRB   = wx.RadioButton(dialog, -1, "Show")
        self.windowHideRB   = wx.RadioButton(dialog, -1, "Hide")

        windowToggleSizer.Add(self.windowToggleRB, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        windowToggleSizer.Add(self.windowShowRB,   0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        windowToggleSizer.Add(self.windowHideRB,   0, wx.ALIGN_CENTER_VERTICAL, 0)

        return windowToggleSizer

    def MakeBindString(self) -> str:
        choice = self.windowToggleTray
        index  = choice.GetSelection()
        windowdesc = choice.GetString(index)
        windowname = self.WindowNames[windowdesc]

        if self.windowShowRB.GetValue():
            return 'show ' + windowname
        elif self.windowHideRB.GetValue():
            return 'windowhide ' + windowname
        else:
            if shortcmd := self.ShortToggleCommands.get(windowdesc, None):
                return shortcmd
            else:
                return 'toggle ' + windowname

    def Serialize(self) -> dict:
        choice = self.windowToggleTray
        if self.windowShowRB.GetValue():
            action = "Show"
        elif self.windowHideRB.GetValue():
            action = "Hide"
        else:
            action = "Toggle"
        return {
                'window': choice.GetString(choice.GetSelection()),
                'action': action,
                }

    def Deserialize(self, init) -> None:
        choice = self.windowToggleTray
        if window := init.get('window', ''):
            if isinstance(window, int):
                choice.SetSelection(window)
            else:
                choice.SetStringSelection(window)

        if choice.GetSelection() == wx.NOT_FOUND:
            choice.SetSelection(0)

        action = init.get('action', '')
        if action == "Show":
            self.windowShowRB.SetValue(True)
        elif action == "Hide":
            self.windowHideRB.SetValue(True)
        else:
            self.windowToggleRB.SetValue(True)

    def OnWindowPicked(self, evt) -> None:
        if evt: evt.Skip()
        wtt = self.windowToggleTray
        enable = self.WindowNames[wtt.GetString(wtt.GetSelection())] != ''

        self.windowShowRB.Enable(enable)
        self.windowHideRB.Enable(enable)
        self.windowToggleRB.Enable(enable)
