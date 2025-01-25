import wx
import UI.EmotePicker
from UI.PowerBinderCommand import PowerBinderCommand

####### Emote
class EmoteCmd(PowerBinderCommand):
    Name = "Emote"
    Menu = "Social"

    def BuildUI(self, dialog):
        emoteSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.emoteText = wx.StaticText(dialog, -1, "Select Emote:")
        emoteSizer.Add(self.emoteText, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)

        self.emoteName = wx.Button(dialog, -1, "...")
        self.emoteName.Bind(wx.EVT_BUTTON, UI.EmotePicker.OnEmotePicker)
        emoteSizer.Add(self.emoteName, 1, wx.ALIGN_CENTER_VERTICAL)

        return emoteSizer

    def MakeBindString(self):
        displayedEmoteName = self.emoteName.GetLabel()
        actualEmotePayload = UI.EmotePicker.payloadMap[displayedEmoteName]

        return actualEmotePayload

    def Serialize(self):
        return {'emoteName': self.emoteName.GetLabel()}

    def Deserialize(self, init):
        if init.get('emoteName', ''): self.emoteName.SetLabel(init['emoteName'])
