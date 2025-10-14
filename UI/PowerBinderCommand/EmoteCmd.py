import wx
import GameData
import UI.EmotePicker
from UI.PowerBinderCommand import PowerBinderCommand

####### Emote
class EmoteCmd(PowerBinderCommand):
    Name = "Emote"
    Menu = "Social"

    def BuildUI(self, dialog) -> wx.BoxSizer:
        emoteSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.emoteText = wx.StaticText(dialog, label = "Select Emote:")
        emoteSizer.Add(self.emoteText, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)

        self.emoteName = wx.Button(dialog, label = "...")
        self.emoteName.Bind(wx.EVT_BUTTON, UI.EmotePicker.OnEmotePicker)
        emoteSizer.Add(self.emoteName, 1, wx.ALIGN_CENTER_VERTICAL)

        return emoteSizer

    def MakeBindString(self) -> str:
        displayedEmoteName = self.emoteName.GetLabel()
        actualEmotePayload = payloadMap[displayedEmoteName]

        return actualEmotePayload

    def Serialize(self) -> dict:
        return {'emoteName': self.emoteName.GetLabel()}

    def Deserialize(self, init) -> None:
        if init.get('emoteName', ''): self.emoteName.SetLabel(init['emoteName'])

# generate the payloadMap at init time instead of lazy-building it.
# This is ugly and fragile.
def AddEmotesString(item):
    if item != "---":
        label, *payload = item.split('%')
        if payload and payload[0]:
            # contains the entire necessary bindstring
            payload = payload[0]
        else:
            label, *payload = item.split('|')
            if payload and payload[0]:
                # contains different string for emote name
                payload = f"em {payload[0]}"
            else:
                # no extra info needed, just lower and de-space the name
                payload = "em " + label.lower().replace(" ","")

        payloadMap[label] = payload

payloadMap = {}
for category in GameData.Emotes['emotes']:
    for _, cat in category.items():
        for subcat in cat:
            if isinstance(subcat, str):
                AddEmotesString(subcat)
            elif isinstance(subcat, dict):
                for _, deepdata in subcat.items():
                    for leafitem in deepdata:
                        if isinstance(leafitem, str):
                            AddEmotesString(leafitem)
                        elif isinstance(leafitem, dict):
                            for _, deeperdata in leafitem.items():
                                for kneelitem in deeperdata:
                                    AddEmotesString(kneelitem)
