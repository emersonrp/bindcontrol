import wx
from UI.PowerBinderCommand import PowerBinderCommand

####### Target Friend
class TargetFriendCmd(PowerBinderCommand):
    Name = "Target Friend"
    Menu = "Targeting"

    def BuildUI(self, dialog):
        targetFriendSizer = wx.BoxSizer(wx.HORIZONTAL)
        targetFriendSizer.Add(wx.StaticText(dialog, -1, "Target Friend:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        self.targetFriendModeChoice = wx.Choice(dialog, -1, choices = ['Near','Far','Next','Prev'])
        self.targetFriendModeChoice.SetSelection(0)
        targetFriendSizer.Add(self.targetFriendModeChoice, 0, wx.ALIGN_CENTER_VERTICAL)

        return targetFriendSizer

    def MakeBindString(self):
        choice = self.targetFriendModeChoice
        index  = choice.GetSelection()
        mode   = choice.GetString(index)

        if self.Profile.Server == "Homecoming":
            return "targetfriend" + mode.lower()
        else: # Rebirth
            return {
                'Near' : 'tgf_n',
                'Far'  : 'tgf_f',
                'Next' : 'tgf_x',
                'Prev' : 'tgf_p',
            }[mode]

    def Serialize(self):
        return { 'mode' : self.targetFriendModeChoice.GetSelection() }

    def Deserialize(self, init):
        if init.get('mode', ''): self.targetFriendModeChoice.SetSelection(init['mode'])
