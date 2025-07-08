import wx
from UI.PowerBinderCommand import PowerBinderCommand

####### Target Enemy
class TargetEnemyCmd(PowerBinderCommand):
    Name = "Target Enemy"
    Menu = "Targeting"

    def BuildUI(self, dialog):
        CenteringSizer = wx.BoxSizer(wx.VERTICAL)

        targetEnemySizer = wx.BoxSizer(wx.HORIZONTAL)
        targetEnemySizer.Add(wx.StaticText(dialog, -1, "Target Enemy:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        self.targetEnemyModeChoice = wx.Choice(dialog, -1, choices = ['Near','Far','Next','Prev'])
        self.targetEnemyModeChoice.SetSelection(0)
        targetEnemySizer.Add(self.targetEnemyModeChoice, 0, wx.ALIGN_CENTER_VERTICAL)

        CenteringSizer.Add(targetEnemySizer, 1, wx.ALIGN_CENTER_HORIZONTAL)
        return CenteringSizer

    def MakeBindString(self):
        choice = self.targetEnemyModeChoice
        index  = choice.GetSelection()
        mode   = choice.GetString(index)

        if self.Profile.Server == "Homecoming":
            return "targetenemy" + mode.lower()
        else: # Rebirth
            return {
                'Near' : 'tge_n',
                'Far'  : 'tge_f',
                'Next' : 'tge_x',
                'Prev' : 'tge_p',
            }[mode]

    def Serialize(self):
        return { 'mode' : self.targetEnemyModeChoice.GetSelection() }

    def Deserialize(self, init):
        if init.get('mode', ''): self.targetEnemyModeChoice.SetSelection(init['mode'])
