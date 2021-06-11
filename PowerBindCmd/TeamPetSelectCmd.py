from PowerBindCmd import PowerBindCmd
import wx


####### Team/Pet Select
class TeamPetSelectCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        teamPetSelectSizer = wx.BoxSizer(wx.HORIZONTAL)
        teamPetSelectSizer.Add(wx.RadioButton(dialog, -1, "Teammate", style=wx.RB_GROUP|wx.ALIGN_CENTER_VERTICAL))
        teamPetSelectSizer.Add(wx.RadioButton(dialog, -1, "Pet/Henchman", style=wx.ALIGN_CENTER_VERTICAL))
        teamPetSelectNumber = wx.SpinCtrl(dialog, -1, style=wx.SP_ARROW_KEYS|wx.ALIGN_CENTER_VERTICAL)
        teamPetSelectNumber.SetRange(1, 7)
        teamPetSelectSizer.Add(teamPetSelectNumber)

        return teamPetSelectSizer

