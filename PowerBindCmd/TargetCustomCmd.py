from PowerBindCmd import PowerBindCmd
import wx

####### Target Custom
class TargetCustomCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

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

    def MakeBindString(self, dialog):
        choice = self.targetCustomModeChoice
        index  = choice.GetSelection()
        mode   = choice.GetString(index)
        targetCommand = "targetcustom" + lower(mode)

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
