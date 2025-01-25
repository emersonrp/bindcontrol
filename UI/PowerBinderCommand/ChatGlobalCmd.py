import wx
from UI.PowerBinderCommand import PowerBinderCommand

####### Chat Command Global
class ChatGlobalCmd(PowerBinderCommand):
    Name = "Chat Command (Global)"
    Menu = "Social"

    def BuildUI(self, dialog):
        chatCommandGlobalSizer = wx.GridBagSizer(5,5)

        self.chatCommandGlobalUseBeginchatCB = wx.CheckBox(dialog, -1, "Use beginchat")
        chatCommandGlobalSizer.Add(self.chatCommandGlobalUseBeginchatCB, (0,0), (1,2))

        self.chatCommandGlobalChannel = wx.TextCtrl(dialog, -1)
        self.chatCommandGlobalChannel.SetHint("Channel")
        chatCommandGlobalSizer.Add(self.chatCommandGlobalChannel, (1,0))

        self.chatCommandGlobalMessage = wx.TextCtrl(dialog, -1)
        self.chatCommandGlobalMessage.SetHint('Chat Command (Global) Message')
        chatCommandGlobalSizer.Add(self.chatCommandGlobalMessage, (1,1), flag=wx.EXPAND)

        chatCommandGlobalSizer.AddGrowableCol(1)

        return chatCommandGlobalSizer

    def MakeBindString(self):
        useBeginchat = self.chatCommandGlobalUseBeginchatCB.IsChecked()
        channel      = self.chatCommandGlobalChannel.GetValue()
        message      = self.chatCommandGlobalMessage.GetValue()

        preface = "beginchat /" if useBeginchat else ""

        return f'{preface}send "{channel}" {message}'

    def Serialize(self):
        return {
            'usebeginchat': self.chatCommandGlobalUseBeginchatCB.GetValue(),
            'channel'     : self.chatCommandGlobalChannel.GetValue(),
            'message'     : self.chatCommandGlobalMessage.GetValue(),
        }

    def Deserialize(self, init):
        if init.get('usebeginchat', ''): self.chatCommandGlobalUseBeginchatCB.SetValue(init['usebeginchat'])
        if init.get('channel',      ''): self.chatCommandGlobalChannel.SetValue(init['channel'])
        if init.get('message',      ''): self.chatCommandGlobalMessage.SetValue(init['message'])
