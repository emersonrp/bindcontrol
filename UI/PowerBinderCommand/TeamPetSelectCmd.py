import wx
from UI.PowerBinderCommand import PowerBinderCommand

####### Team/Pet Select
class TeamPetSelectCmd(PowerBinderCommand):
    Name = "Team/Pet Select"
    Menu = "Targeting"

    def BuildUI(self, dialog):
        CenteringSizer = wx.BoxSizer(wx.VERTICAL)

        teamPetSelectSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.teamPetSelectTeamRB = wx.RadioButton(dialog, -1, "Teammate", style=wx.RB_GROUP|wx.ALIGN_CENTER_VERTICAL)
        teamPetSelectSizer.Add(self.teamPetSelectTeamRB, 0, wx.ALIGN_CENTER_VERTICAL)

        self.teamPetSelectPetRB  = wx.RadioButton(dialog, -1, "Pet/Henchman", style=wx.ALIGN_CENTER_VERTICAL)
        teamPetSelectSizer.Add(self.teamPetSelectPetRB, 0, wx.ALIGN_CENTER_VERTICAL)

        self.teamPetSelectNumber = wx.Choice(dialog, -1, choices=['1','2','3','4','5','6','7','8'],
                style=wx.ALIGN_CENTER_VERTICAL)
        self.teamPetSelectNumber.SetSelection(0)
        teamPetSelectSizer.Add(self.teamPetSelectNumber, 0, wx.ALIGN_CENTER_VERTICAL)

        CenteringSizer.Add(teamPetSelectSizer, 1, wx.ALIGN_CENTER_HORIZONTAL)
        return CenteringSizer

    def MakeBindString(self):
        teamOrPet = 'team' if self.teamPetSelectTeamRB.GetValue() else 'pet'
        targetNumber = self.teamPetSelectNumber.GetSelection()+1

        return f"{teamOrPet}select {targetNumber}"

    def Serialize(self):
        return {
            'teamOrPet': 'team' if self.teamPetSelectTeamRB.GetValue() else 'pet',
            'targetNum': self.teamPetSelectNumber.GetSelection(),
        }

    def Deserialize(self, init):
        ToP = init.get('teamOrPet', '')
        if ToP == 'pet':
            self.teamPetSelectPetRB.SetValue(True)
        else:
            self.teamPetSelectTeamRB.SetValue(True)
        if init.get('targetNum', ''): self.teamPetSelectNumber.SetSelection(init['targetNum'])
