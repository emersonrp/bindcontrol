from PowerBindCmd import PowerBindCmd
import wx


####### Team/Pet Select
class TeamPetSelectCmd(PowerBindCmd):
    def BuildUI(self, dialog):
        teamPetSelectSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.teamPetSelectTeamRB = wx.RadioButton(dialog, -1, "Teammate", style=wx.RB_GROUP|wx.ALIGN_CENTER_VERTICAL)
        teamPetSelectSizer.Add(self.teamPetSelectTeamRB, 0, wx.ALIGN_CENTER_VERTICAL)

        self.teamPetSelectPetRB  = wx.RadioButton(dialog, -1, "Pet/Henchman", style=wx.ALIGN_CENTER_VERTICAL)
        teamPetSelectSizer.Add(self.teamPetSelectPetRB, 0, wx.ALIGN_CENTER_VERTICAL)

        self.teamPetSelectNumber = wx.Choice(dialog, -1, choices=['1','2','3','4','5','6','7','8'],
                style=wx.ALIGN_CENTER_VERTICAL)
        self.teamPetSelectNumber.SetSelection(0)
        teamPetSelectSizer.Add(self.teamPetSelectNumber, 0, wx.ALIGN_CENTER_VERTICAL)

        return teamPetSelectSizer

    def MakeBindString(self, dialog):
        teamOrPet = 'team' if self.teamPetSelectTeamRB.GetValue() else 'pet'
        targetNumber = self.teamPetSelectNumber.GetSelection()+1

        return f"{teamOrPet}select {targetNumber}"
