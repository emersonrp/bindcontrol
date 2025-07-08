import wx
from UI.PowerBinderCommand import PowerBinderCommand

####### Target Custom
class TargetCustomCmd(PowerBinderCommand):
    Name = "Target Custom"
    Menu = "Targeting"

    def BuildUI(self, dialog):
        CenteringSizer = wx.BoxSizer(wx.VERTICAL)
        targetCustomSizer = wx.GridBagSizer(5,5)
        targetCustomSizer.Add(wx.StaticText(dialog, -1, "Target Mode:"), (0,0),
                flag =wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.RIGHT)
        self.targetCustomModeChoice = wx.Choice(dialog, -1, choices = ['Near','Far','Next','Prev'])
        self.targetCustomModeChoice.SetSelection(0)
        targetCustomSizer.Add(self.targetCustomModeChoice, (0,1), flag=wx.EXPAND)
        self.targetCustomOptionalName = wx.TextCtrl(dialog, -1)
        self.targetCustomOptionalName.SetHint("Optional name to match")
        targetCustomSizer.Add(self.targetCustomOptionalName, (0,2), flag=wx.EXPAND)
        self.targetCustomCBEnemies = wx.CheckBox(dialog, -1, "Enemies")
        targetCustomSizer.Add(self.targetCustomCBEnemies, (1,1))
        self.targetCustomCBFriends = wx.CheckBox(dialog, -1, "Friends")
        targetCustomSizer.Add(self.targetCustomCBFriends, (1,2))
        self.targetCustomCBDefeated = wx.CheckBox(dialog, -1, "Defeated")
        targetCustomSizer.Add(self.targetCustomCBDefeated, (2,1))
        self.targetCustomCBAlive = wx.CheckBox(dialog, -1, "Alive")
        targetCustomSizer.Add(self.targetCustomCBAlive, (2,2))
        self.targetCustomCBMyPets = wx.CheckBox(dialog, -1, "My Pets")
        targetCustomSizer.Add(self.targetCustomCBMyPets, (3,1))
        self.targetCustomCBNotMyPets = wx.CheckBox(dialog, -1, "Not My Pets")
        targetCustomSizer.Add(self.targetCustomCBNotMyPets, (3,2))
        self.targetCustomCBBaseItems = wx.CheckBox(dialog, -1, "Base Items")
        targetCustomSizer.Add(self.targetCustomCBBaseItems, (4,1))
        self.targetCustomCBNotBaseItems = wx.CheckBox(dialog, -1, "Not Base Items")
        targetCustomSizer.Add(self.targetCustomCBNotBaseItems, (4,2))
        self.targetCustomCBTeammates = wx.CheckBox(dialog, -1, "Teammates")
        targetCustomSizer.Add(self.targetCustomCBTeammates, (5,1))
        self.targetCustomCBNotTeammates = wx.CheckBox(dialog, -1, "Not Teammates")
        targetCustomSizer.Add(self.targetCustomCBNotTeammates, (5,2))

        targetCustomSizer.AddGrowableCol(2)

        CenteringSizer.Add(targetCustomSizer, 0, wx.ALIGN_CENTER_HORIZONTAL)
        return CenteringSizer

    def MakeBindString(self):
        choice = self.targetCustomModeChoice
        index  = choice.GetSelection()
        mode   = choice.GetString(index)

        if self.Profile.Server == 'Homecoming':
            targetCommand = "targetcustom" + mode.lower()
        else: # Rebirth
            targetCommand = "tgt_" + {
                'Near' : 'n',
                'Far'  : 'f',
                'Next' : 'x',
                'Prev' : 'p'
            }[mode]

        enemy       = self.GetServerCommand("enemy")       if self.targetCustomCBEnemies.     IsChecked() else ""
        friend      = self.GetServerCommand("friend")      if self.targetCustomCBFriends.     IsChecked() else ""
        defeated    = self.GetServerCommand("defeated")    if self.targetCustomCBDefeated.    IsChecked() else ""
        alive       = self.GetServerCommand("alive")       if self.targetCustomCBAlive.       IsChecked() else ""
        mypet       = self.GetServerCommand("mypet")       if self.targetCustomCBMyPets.      IsChecked() else ""
        notmypet    = self.GetServerCommand("notmypet")    if self.targetCustomCBNotMyPets.   IsChecked() else ""
        base        = self.GetServerCommand("base")        if self.targetCustomCBBaseItems.   IsChecked() else ""
        notbase     = self.GetServerCommand("notbase")     if self.targetCustomCBNotBaseItems.IsChecked() else ""
        teammate    = self.GetServerCommand("teammate")    if self.targetCustomCBTeammates.   IsChecked() else ""
        notteammate = self.GetServerCommand("notteammate") if self.targetCustomCBNotTeammates.IsChecked() else ""

        name = self.targetCustomOptionalName.GetValue()

        return f"{targetCommand}{enemy}{friend}{defeated}{alive}{mypet}{notmypet}{base}{notbase}{teammate}{notteammate} {name}"

    def Serialize(self):
        return {
            'mode'        : self.targetCustomModeChoice.GetSelection(),
            'enemy'       : self.targetCustomCBEnemies.     IsChecked(),
            'friend'      : self.targetCustomCBFriends.     IsChecked(),
            'defeated'    : self.targetCustomCBDefeated.    IsChecked(),
            'alive'       : self.targetCustomCBAlive.       IsChecked(),
            'mypet'       : self.targetCustomCBMyPets.      IsChecked(),
            'notmypet'    : self.targetCustomCBNotMyPets.   IsChecked(),
            'base'        : self.targetCustomCBBaseItems.   IsChecked(),
            'notbase'     : self.targetCustomCBNotBaseItems.IsChecked(),
            'teammate'    : self.targetCustomCBTeammates.   IsChecked(),
            'notteammate' : self.targetCustomCBNotTeammates.IsChecked(),
            'name'        : self.targetCustomOptionalName.GetValue(),
        }

    def Deserialize(self, init):
        if init.get('mode'        , ''): self.targetCustomModeChoice.SetSelection(init['mode'])
        if init.get('enemy'       , ''): self.targetCustomCBEnemies.     SetValue(init['enemy'])
        if init.get('friend'      , ''): self.targetCustomCBFriends.     SetValue(init['friend'])
        if init.get('defeated'    , ''): self.targetCustomCBDefeated.    SetValue(init['defeated'])
        if init.get('alive'       , ''): self.targetCustomCBAlive.       SetValue(init['alive'])
        if init.get('mypet'       , ''): self.targetCustomCBMyPets.      SetValue(init['mypet'])
        if init.get('notmypet'    , ''): self.targetCustomCBNotMyPets.   SetValue(init['notmypet'])
        if init.get('base'        , ''): self.targetCustomCBBaseItems.   SetValue(init['base'])
        if init.get('notbase'     , ''): self.targetCustomCBNotBaseItems.SetValue(init['notbase'])
        if init.get('teammate'    , ''): self.targetCustomCBTeammates.   SetValue(init['teammate'])
        if init.get('notteammate' , ''): self.targetCustomCBNotTeammates.SetValue(init['notteammate'])
        if init.get('name'        , ''): self.targetCustomOptionalName.SetValue(init['name'])

    def GetServerCommand(self, command):
        server = self.Profile.Server
        if server == 'Homecoming': return f" {command}"

        # Rebirth abbreviations
        return {
            'enemy'       : ' em',
            'friend'      : ' fd',
            'defeated'    : ' dd',
            'alive'       : ' ae',
            'mypet'       : ' mp',
            'notmypet'    : ' np',
            'base'        : ' bc',
            'notbase'     : ' bn',
            'teammate'    : ' tm',
            'notteammate' : ' tn',
        }[command]
