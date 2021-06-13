from PowerBindCmd import PowerBindCmd
import wx
import GameData

#######Costume Change
class CostumeChangeCmd(PowerBindCmd):
    def BuildUI(self, dialog):
        costumeChangeSizer = wx.BoxSizer(wx.HORIZONTAL)
        costumeChangeSizer.Add(wx.StaticText(dialog, -1, "Costume:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        self.costumeChangeCostume = wx.Choice(dialog, -1,
               choices = ["First", "Second", "Third", "Fourth", "Fifth"])
        self.costumeChangeCostume.SetSelection(0)
        costumeChangeSizer.Add(self.costumeChangeCostume, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        costumeChangeSizer.Add(wx.StaticText(dialog, -1, "CC Emote:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        self.costumeChangeEmote = wx.Choice(dialog, -1,
                choices = GameData.Emotes['costumechange'])
        self.costumeChangeEmote.Insert("- None -", 0)
        self.costumeChangeEmote.SetSelection(0)
        costumeChangeSizer.Add(self.costumeChangeEmote, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        return costumeChangeSizer

    def MakeBindString(self, dialog):
        costumeNumber = self.costumeChangeCostume.GetSelection() + 1
        costumeEmote  = self.costumeChangeEmote.GetSelection()

        print(f"costumeEmote is {costumeEmote}")
        if costumeEmote: # None, or 0 == "- None -"
            ccCmd = 'cce'
            emoteName = self.costumeChangeEmote.GetString(costumeEmote)
            emoteName = " CC" + emoteName.replace(" ","")
        else:
            ccCmd = 'cc'
            emoteName = ''


        return f"{ccCmd} {costumeNumber}{emoteName}"
