import wx
import GameData
from UI.PowerBinderCommand import PowerBinderCommand

#######Costume Change
class CostumeChangeCmd(PowerBinderCommand):
    Name = "Costume Change"
    Menu = "Social"

    def BuildUI(self, dialog) -> wx.BoxSizer:
        costumeChangeSizer = wx.BoxSizer(wx.HORIZONTAL)
        costumeChangeSizer.Add(wx.StaticText(dialog, -1, "Costume:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        self.costumeChangeCostume = wx.Choice(dialog, -1,
               choices = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth", "Ninth", "Tenth"])
        self.costumeChangeCostume.SetSelection(0)
        costumeChangeSizer.Add(self.costumeChangeCostume, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        costumeChangeSizer.Add(wx.StaticText(dialog, -1, "CC Emote:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        self.costumeChangeEmote = wx.Choice(dialog, -1,
                choices = GameData.Emotes['costumechange'])
        self.costumeChangeEmote.Insert("- None -", 0)
        self.costumeChangeEmote.SetSelection(0)
        costumeChangeSizer.Add(self.costumeChangeEmote, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        return costumeChangeSizer

    def MakeBindString(self) -> str:
        costumeNumber = self.costumeChangeCostume.GetSelection()
        costumeEmote  = self.costumeChangeEmote.GetSelection()

        if costumeEmote: # None, or 0 == "- None -"
            ccCmd = 'cce'
            emoteName = self.costumeChangeEmote.GetString(costumeEmote)
            emoteName = " CC" + emoteName.replace(" ","")
        else:
            ccCmd = 'cc'
            emoteName = ''

        return f"{ccCmd} {costumeNumber}{emoteName}"

    def Serialize(self) -> dict:
        return{
            'costumeNumber': self.costumeChangeCostume.GetSelection(),
            'costumeEmote' : self.costumeChangeEmote.GetSelection(),
        }

    def Deserialize(self, init) -> None:
        if init.get('costumeNumber', ''): self.costumeChangeCostume.SetSelection(init['costumeNumber'])
        if init.get('costumeEmote' , ''): self.costumeChangeEmote  .SetSelection(init['costumeEmote'])
