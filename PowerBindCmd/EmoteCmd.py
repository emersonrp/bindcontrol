from PowerBindCmd import PowerBindCmd
import wx

####### Emote
class EmoteCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        emoteSizer = wx.BoxSizer(wx.HORIZONTAL)
        emoteSizer.Add(wx.StaticText(dialog, -1, "Emote:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        # TODO - make this a wx.Choice with a list?  Yikes that's a big list.
        self.emoteName = wx.TextCtrl(dialog, -1)
        emoteSizer.Add(self.emoteName, 1, wx.ALIGN_CENTER_VERTICAL)

        return emoteSizer

    def MakeBindString(self, dialog):
        return f"em {self.emoteName.GetValue()}"
