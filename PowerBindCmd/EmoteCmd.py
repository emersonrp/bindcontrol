from PowerBindCmd import PowerBindCmd
import UI
import UI.EmotePicker
from UI.EmotePicker import EmotePicker
import wx

####### Emote
class EmoteCmd(PowerBindCmd):
    def BuildUI(self, dialog):
        emoteSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.emoteText = wx.StaticText(dialog, -1, "Select Emote:")
        emoteSizer.Add(self.emoteText, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)

        self.emoteName = wx.Button(dialog, -1, "...")
        self.emoteName.Bind(wx.EVT_BUTTON, UI.EmotePicker.OnEmotePicker)
        emoteSizer.Add(self.emoteName, 1, wx.ALIGN_CENTER_VERTICAL)

        return emoteSizer

    def MakeBindString(self, dialog):
        displayedEmoteName = self.emoteName.GetLabel()
        actualEmotePayload = EmotePicker.payloadMap[displayedEmoteName]

        return actualEmotePayload
