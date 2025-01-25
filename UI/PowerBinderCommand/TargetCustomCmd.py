import wx
from UI.PowerBinderCommand import PowerBinderCommand

####### Target Custom
class TargetCustomCmd(PowerBinderCommand):
    Name = "Target Custom"
    Menu = "Targeting"

    def BuildUI(self, dialog):
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
        targetCustomSizer.Add(self.targetCustomCBEnemies, (1,0))
        self.targetCustomCBFriends = wx.CheckBox(dialog, -1, "Friends")
        targetCustomSizer.Add(self.targetCustomCBFriends, (1,1))
        self.targetCustomCBDefeated = wx.CheckBox(dialog, -1, "Defeated")
        targetCustomSizer.Add(self.targetCustomCBDefeated, (2,0))
        self.targetCustomCBAlive = wx.CheckBox(dialog, -1, "Alive")
        targetCustomSizer.Add(self.targetCustomCBAlive, (2,1))
        self.targetCustomCBMyPets = wx.CheckBox(dialog, -1, "My Pets")
        targetCustomSizer.Add(self.targetCustomCBMyPets, (3,0))
        self.targetCustomCBNotMyPets = wx.CheckBox(dialog, -1, "Not My Pets")
        targetCustomSizer.Add(self.targetCustomCBNotMyPets, (3,1))
        self.targetCustomCBBaseItems = wx.CheckBox(dialog, -1, "Base Items")
        targetCustomSizer.Add(self.targetCustomCBBaseItems, (4,0))
        self.targetCustomCBNotBaseItems = wx.CheckBox(dialog, -1, "Not Base Items")
        targetCustomSizer.Add(self.targetCustomCBNotBaseItems, (4,1))

        targetCustomSizer.AddGrowableCol(2)

        return targetCustomSizer

    def MakeBindString(self):
        choice = self.targetCustomModeChoice
        index  = choice.GetSelection()
        mode   = choice.GetString(index)
        targetCommand = "targetcustom" + mode.lower()

        enemy    = " enemy"    if self.targetCustomCBEnemies.      IsChecked() else ""
        friend   = " friend"   if self.targetCustomCBFriends.      IsChecked() else ""
        defeated = " defeated" if self.targetCustomCBDefeated.     IsChecked() else ""
        alive    = " alive"    if self.targetCustomCBAlive.        IsChecked() else ""
        mypet    = " mypet"    if self.targetCustomCBMyPets.       IsChecked() else ""
        notmypet = " notmypet" if self.targetCustomCBNotMyPets.    IsChecked() else ""
        base     = " base"     if self.targetCustomCBBaseItems.    IsChecked() else ""
        notbase  = " notbase"  if self.targetCustomCBNotBaseItems. IsChecked() else ""

        name = self.targetCustomOptionalName.GetValue()

        return f"{targetCommand}{enemy}{friend}{defeated}{alive}{mypet}{notmypet}{base}{notbase} {name}"

    def Serialize(self):
        return {
            'mode'     : self.targetCustomModeChoice.GetSelection(),
            'enemy'    : self.targetCustomCBEnemies.     IsChecked(),
            'friend'   : self.targetCustomCBFriends.     IsChecked(),
            'defeated' : self.targetCustomCBDefeated.    IsChecked(),
            'alive'    : self.targetCustomCBAlive.       IsChecked(),
            'mypet'    : self.targetCustomCBMyPets.      IsChecked(),
            'notmypet' : self.targetCustomCBNotMyPets.   IsChecked(),
            'base'     : self.targetCustomCBBaseItems.   IsChecked(),
            'notbase'  : self.targetCustomCBNotBaseItems.IsChecked(),
            'name'     : self.targetCustomOptionalName.GetValue(),
        }

    def Deserialize(self, init):
        if init.get('mode'    , ''): self.targetCustomModeChoice.SetSelection(init['mode'])
        if init.get('enemy'   , ''): self.targetCustomCBEnemies.     SetValue(init['enemy'])
        if init.get('friend'  , ''): self.targetCustomCBFriends.     SetValue(init['friend'])
        if init.get('defeated', ''): self.targetCustomCBDefeated.    SetValue(init['defeated'])
        if init.get('alive'   , ''): self.targetCustomCBAlive.       SetValue(init['alive'])
        if init.get('mypet'   , ''): self.targetCustomCBMyPets.      SetValue(init['mypet'])
        if init.get('notmypet', ''): self.targetCustomCBNotMyPets.   SetValue(init['notmypet'])
        if init.get('base'    , ''): self.targetCustomCBBaseItems.   SetValue(init['base'])
        if init.get('notbase' , ''): self.targetCustomCBNotBaseItems.SetValue(init['notbase'])
        if init.get('name'    , ''): self.targetCustomOptionalName.SetValue(init['name'])
